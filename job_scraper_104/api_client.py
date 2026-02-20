"""
104 人力銀行 API 客戶端模組（混合方案版本）
使用 Playwright CDP 抓取職缺列表 + requests 抓取詳情
"""

import requests
import time
import random
import logging
import re
import asyncio
from typing import Dict, List, Optional
from playwright.async_api import async_playwright
from . import config

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Job104APIClient:
    """104 人力銀行 API 客戶端（混合方案）"""
    
    def __init__(self, use_cdp: bool = True, cdp_url: str = "http://localhost:9527"):
        """
        初始化 API 客戶端
        
        Args:
            use_cdp: 是否使用 CDP 連接（預設 True）
            cdp_url: CDP 連接 URL
        """
        self.session = requests.Session()
        self.use_cdp = use_cdp
        self.cdp_url = cdp_url
        
        # 完整的瀏覽器 Headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
    def _delay(self, delay_range: tuple):
        """隨機延遲"""
        delay_time = random.uniform(delay_range[0], delay_range[1])
        logger.debug(f"延遲 {delay_time:.2f} 秒...")
        time.sleep(delay_time)
    
    async def search_jobs_with_cdp(
        self, 
        keyword: str, 
        page: int = 1,
        max_jobs: int = 50
    ) -> List[str]:
        """
        使用 Playwright CDP 搜尋職缺並返回職缺 ID 列表
        
        Args:
            keyword: 搜尋關鍵字
            page: 頁碼（暫不使用，CDP 方案直接抓取所有可見職缺）
            max_jobs: 最大職缺數
        
        Returns:
            職缺 ID 列表
        """
        logger.info(f"使用 CDP 搜尋職缺：關鍵字='{keyword}', 最大數量={max_jobs}")
        
        job_ids = []
        
        async with async_playwright() as p:
            try:
                # 連接到 CDP
                browser = await p.chromium.connect_over_cdp(self.cdp_url)
                context = browser.contexts[0]
                page_obj = context.pages[0] if context.pages else await context.new_page()
                
                # 導航到搜尋頁面
                search_url = f"https://www.104.com.tw/jobs/search/?keyword={keyword}&page={page}"
                logger.info(f"導航到: {search_url}")
                
                await page_obj.goto(search_url, wait_until='domcontentloaded', timeout=60000)
                await asyncio.sleep(5)  # 等待頁面穩定
                
                # 滾動頁面以載入更多職缺
                await page_obj.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                await asyncio.sleep(2)
                
                # 從所有連結中提取職缺 ID
                job_ids = await page_obj.evaluate("""
                    () => {
                        const links = document.querySelectorAll('a[href]');
                        const ids = [];
                        links.forEach(link => {
                            const href = link.getAttribute('href');
                            // 匹配 job%2F8lhbs 或 /job/8lhbs 格式
                            let match = href.match(/job%2F([a-z0-9]+)/);
                            if (match && match[1]) {
                                ids.push(match[1]);
                            } else {
                                match = href.match(/\\/job\\/([a-z0-9]+)/);
                                if (match && match[1]) {
                                    ids.push(match[1]);
                                }
                            }
                        });
                        return [...new Set(ids)]; // 去重
                    }
                """)
                
                logger.info(f"成功取得 {len(job_ids)} 個職缺 ID")
                
                # 延遲
                self._delay(config.REQUEST_DELAY_LIST)
                
                return job_ids[:max_jobs]
                
            except Exception as e:
                logger.error(f"CDP 搜尋失敗: {e}")
                return []
    
    def get_job_detail(self, job_id: str) -> Optional[Dict]:
        """
        使用 requests 取得職缺詳細資訊
        
        Args:
            job_id: 職缺 ID
        
        Returns:
            包含職缺詳細資訊的字典
        """
        url = f"{config.API_BASE_URL}{config.API_JOB_DETAIL_ENDPOINT}/{job_id}"
        job_url = f"{config.API_BASE_URL}/job/{job_id}"
        
        headers = {
            'Referer': job_url,
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        try:
            logger.info(f"正在取得職缺詳情：job_id={job_id}")
            response = self.session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                # 提取各個部分的資料
                header = data['data'].get('header', {})
                job_detail = data['data'].get('jobDetail', {})
                condition = data['data'].get('condition', {})
                
                # 整理職缺資訊
                job_info = {
                    'job_id': job_id,
                    'title': header.get('jobName', job_detail.get('jobName', '未提供')),
                    'company': header.get('custName', job_detail.get('custName', '未提供')),
                    'salary': job_detail.get('salary', '面議'),
                    'location': f"{job_detail.get('addressRegion', '')}{job_detail.get('addressDetail', '')}".strip() or '未提供',
                    'job_description': job_detail.get('jobDescription', ''),
                    'education': condition.get('edu', '未指定'),
                    'experience': condition.get('workExp', '未指定'),
                    'skills': [],  # 可從其他欄位提取
                    'specialty': self._extract_specialty(condition.get('specialty', [])),
                    'other_requirement': condition.get('other', ''),
                    'keywords': header.get('jobNameKeyword', []) if isinstance(header.get('jobNameKeyword'), list) else [],
                    'appear_date': header.get('appearDate', ''),
                    'job_url': job_url,
                }
                
                logger.info(f"成功取得職缺詳情：{job_info['title']}")
                
                # 延遲
                self._delay(config.REQUEST_DELAY_DETAIL)
                
                return job_info
            else:
                logger.warning(f"職缺詳情格式異常：{data}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"請求超時：{url}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP 錯誤 ({e.response.status_code}): {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"請求失敗: {e}")
            return None
        except ValueError as e:
            logger.error(f"JSON 解析失敗: {e}")
            return None
    
    def _extract_specialty(self, specialty_raw) -> List[str]:
        """提取擅長工具列表"""
        if isinstance(specialty_raw, list):
            return [s.get('description', '') for s in specialty_raw if isinstance(s, dict) and s.get('description')]
        return []
    
    def close(self):
        """關閉 session"""
        self.session.close()
        logger.info("API 客戶端已關閉")
