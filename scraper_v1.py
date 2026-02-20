"""
主要爬蟲協調模組（混合方案版本）
使用 Playwright CDP 抓取列表 + requests 抓取詳情
"""

import logging
import asyncio
from typing import Set, List, Dict
from .api_client import Job104APIClient
from .keyword_linker import KeywordLinker
from .obsidian_formatter import ObsidianFormatter
from . import config

logger = logging.getLogger(__name__)


class JobScraper:
    """104 職缺爬蟲（混合方案）"""
    
    def __init__(self, use_cdp: bool = True, cdp_url: str = "http://localhost:9527"):
        """
        初始化爬蟲
        
        Args:
            use_cdp: 是否使用 CDP 連接
            cdp_url: CDP 連接 URL
        """
        self.api_client = Job104APIClient(use_cdp=use_cdp, cdp_url=cdp_url)
        self.keyword_linker = KeywordLinker()
        self.formatter = ObsidianFormatter()
        self.scraped_job_ids: Set[str] = set()  # 記錄已抓取的職缺 ID
    
    async def scrape_keyword_async(self, keyword: str, max_jobs: int = 50) -> List[Dict]:
        """
        爬取指定關鍵字的職缺（異步版本）
        
        Args:
            keyword: 搜尋關鍵字
            max_jobs: 最大職缺數
        
        Returns:
            職缺資料清單
        """
        logger.info(f"========== 開始爬取關鍵字：{keyword} ==========")
        
        jobs = []
        page = 1
        
        while len(jobs) < max_jobs:
            logger.info(f"正在爬取第 {page} 頁...")
            
            # 使用 CDP 搜尋職缺列表
            job_ids = await self.api_client.search_jobs_with_cdp(
                keyword=keyword,
                page=page,
                max_jobs=max_jobs - len(jobs)  # 只抓取還需要的數量
            )
            
            if not job_ids:
                logger.warning(f"第 {page} 頁無職缺，停止爬取")
                break
            
            # 遍歷每個職缺 ID
            for job_id in job_ids:
                # 去重檢查
                if config.ENABLE_DEDUPLICATION and job_id in self.scraped_job_ids:
                    logger.debug(f"職缺 {job_id} 已抓取，跳過")
                    continue
                
                # 取得職缺詳情（使用 requests）
                job_data = self.api_client.get_job_detail(job_id)
                if not job_data:
                    logger.warning(f"無法取得職缺詳情：{job_id}")
                    continue
                
                # 技術名詞處理（加上連結並學習新關鍵字）
                job_data = self.keyword_linker.process_job_data(job_data)
                
                # 加入結果清單
                jobs.append(job_data)
                self.scraped_job_ids.add(job_id)
                
                logger.info(f"已抓取 {len(jobs)}/{max_jobs} 筆職缺：{job_data['title']}")
                
                # 檢查是否已達目標數量
                if len(jobs) >= max_jobs:
                    break
            
            # 如果這一頁沒有新職缺，停止翻頁
            if len(jobs) == 0 or len(job_ids) == 0:
                break
            
            # 翻到下一頁
            page += 1
            
            # 避免無限迴圈（最多爬取 10 頁）
            if page > 10:
                logger.warning("已達最大頁數限制（10 頁），停止爬取")
                break
        
        logger.info(f"========== 完成爬取關鍵字：{keyword}，共 {len(jobs)} 筆 ==========")
        return jobs
    
    def scrape_keyword(self, keyword: str, max_jobs: int = 50) -> List[Dict]:
        """
        爬取指定關鍵字的職缺（同步包裝）
        
        Args:
            keyword: 搜尋關鍵字
            max_jobs: 最大職缺數
        
        Returns:
            職缺資料清單
        """
        return asyncio.run(self.scrape_keyword_async(keyword, max_jobs))
    
    async def scrape_all_async(self):
        """爬取所有關鍵字的職缺並儲存為 Obsidian 筆記（異步版本）"""
        logger.info("********** 開始執行 104 職缺爬蟲（混合方案）**********")
        
        for keyword in config.KEYWORDS:
            try:
                # 爬取職缺
                jobs = await self.scrape_keyword_async(keyword, config.MAX_JOBS_PER_KEYWORD)
                
                # 儲存為 Obsidian 筆記
                for job_data in jobs:
                    self.formatter.save_job_note(job_data, keyword)
                
                logger.info(f"關鍵字「{keyword}」已完成，共儲存 {len(jobs)} 筆筆記")
                
            except Exception as e:
                logger.error(f"爬取關鍵字「{keyword}」時發生錯誤：{e}")
                import traceback
                traceback.print_exc()
                continue
        
        logger.info("********** 所有爬取任務已完成 **********")
        
        # 關閉 API 客戶端
        self.api_client.close()
    
    def scrape_all(self):
        """爬取所有關鍵字的職缺並儲存為 Obsidian 筆記（同步包裝）"""
        asyncio.run(self.scrape_all_async())
