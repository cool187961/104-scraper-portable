"""
使用 CDP 連接現有 Chrome + Playwright 抓取職缺 URL
然後使用 requests 爬取詳情
"""

import sys
import os
import asyncio
import re
from typing import List, Dict

# 設定 UTF-8 編碼
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.async_api import async_playwright
import requests


async def get_job_urls_with_playwright(keyword: str, max_jobs: int = 10) -> List[str]:
    """
    使用 Playwright 連接 CDP 並抓取職缺 URL 列表
    
    Args:
        keyword: 搜尋關鍵字
        max_jobs: 最大職缺數
    
    Returns:
        職缺 URL 列表
    """
    print(f"========== 使用 Playwright CDP 抓取職缺列表 ==========")
    print(f"關鍵字: {keyword}")
    print(f"目標數量: {max_jobs}\n")
    
    job_urls = []
    
    async with async_playwright() as p:
        try:
            # 連接到已開啟的 Chrome（使用 CDP）
            print("1. 正在連接到 Chrome (CDP: localhost:9527)...")
            browser = await p.chromium.connect_over_cdp("http://localhost:9527")
            print("   [成功] 已連接到 Chrome\n")
            
            # 取得第一個 context（或創建新的）
            contexts = browser.contexts
            if contexts:
                context = contexts[0]
                print(f"   使用現有 context (共 {len(contexts)} 個)")
            else:
                context = await browser.new_context()
                print("   創建新 context")
            
            # 取得現有頁面或創建新頁面
            pages = context.pages
            if pages:
                page = pages[0]
                print(f"   使用現有頁面 (共 {len(pages)} 個)\n")
            else:
                page = await context.new_page()
                print("   創建新頁面\n")
            
            # 2. 導航到搜尋頁面
            search_url = f"https://www.104.com.tw/jobs/search/?keyword={keyword}"
            print(f"2. 正在導航到: {search_url}")
            
            try:
                await page.goto(search_url, timeout=60000)  # 增加超時到 60 秒
                print("   [成功] 頁面載入完成\n")
            except Exception as e:
                print(f"   [警告] 頁面載入超時，嘗試繼續: {e}\n")
            
            # 等待一下讓頁面穩定
            await asyncio.sleep(3)
            
            # 3. 等待職缺列表載入
            print("3. 等待職缺列表載入...")
            try:
                await page.wait_for_selector('a.jb-link', timeout=15000)
                print("   [成功] 職缺列表已載入\n")
            except Exception as e:
                print(f"   [錯誤] 無法找到職缺列表: {e}")
                print("   嘗試查找其他選擇器...\n")
                
                # 嘗試其他選擇器
                try:
                    await page.wait_for_selector('article[data-job-no]', timeout=10000)
                    print("   [成功] 找到 article 元素\n")
                except:
                    print("   [失敗] 無法找到任何職缺元素\n")
                    return []
            
            # 4. 抓取職缺連結
            print("4. 正在抓取職缺 URL...")
            
            # 嘗試多種選擇器
            selectors = [
                'a.jb-link',
                'a[data-gtm-joblist]',
                'article[data-job-no] a',
                'a[href*="/job/"]'
            ]
            
            job_links = []
            for selector in selectors:
                try:
                    links = await page.query_selector_all(selector)
                    if links:
                        print(f"   使用選擇器: {selector} (找到 {len(links)} 個)")
                        job_links = links
                        break
                except:
                    continue
            
            if not job_links:
                print("   [失敗] 無法找到任何職缺連結\n")
                return []
            
            for link in job_links[:max_jobs]:
                href = await link.get_attribute('href')
                if href and '/job/' in href:
                    # 從重定向 URL 中提取真實的職缺 URL
                    # 例如: https://r.104.com.tw/m104?url=https%3A%2F%2Fwww.104.com.tw%2Fjob%2F8lhbs
                    # 或直接: /job/8lhbs
                    
                    # 方法1: 從 URL 參數提取
                    match = re.search(r'job%2F([a-z0-9]+)', href)
                    if match:
                        job_id = match.group(1)
                    else:
                        # 方法2: 直接從路徑提取
                        match = re.search(r'/job/([a-z0-9]+)', href)
                        if match:
                            job_id = match.group(1)
                        else:
                            continue
                    
                    job_url = f"https://www.104.com.tw/job/{job_id}"
                    if job_url not in job_urls:  # 去重
                        job_urls.append(job_url)
                        print(f"  ✓ 找到職缺: {job_id}")
            
            print(f"\n[成功] 共找到 {len(job_urls)} 個職缺 URL\n")
            
            # 不關閉瀏覽器，保持 CDP 連接
            # await page.close()
            # await browser.close()
            
        except Exception as e:
            print(f"[錯誤] {e}")
            import traceback
            traceback.print_exc()
    
    return job_urls


def get_job_detail_with_requests(job_url: str, cookies: dict = None) -> Dict:
    """
    使用 requests 抓取職缺詳情
    
    Args:
        job_url: 職缺 URL
        cookies: Cookie 字典
    
    Returns:
        職缺詳情資料
    """
    # 從 URL 提取 job_id
    job_id = job_url.split('/')[-1]
    
    # 構建 API URL
    api_url = f"https://www.104.com.tw/job/ajax/content/{job_id}"
    
    # 設定 Headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': job_url,
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    try:
        response = requests.get(api_url, headers=headers, cookies=cookies, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'data' in data:
            job_detail = data['data'].get('jobDetail', {})
            condition = data['data'].get('condition', {})
            
            return {
                'job_id': job_id,
                'job_url': job_url,
                'title': job_detail.get('jobName', 'N/A'),
                'company': job_detail.get('custName', 'N/A'),
                'description': job_detail.get('jobDescription', 'N/A')[:200] + '...',  # 只顯示前 200 字
                'location': f"{job_detail.get('addressRegion', '')}{job_detail.get('addressDetail', '')}",
                'education': condition.get('edu', 'N/A'),
                'experience': condition.get('workExp', 'N/A'),
                'salary': job_detail.get('salary', 'N/A'),
            }
        else:
            return None
            
    except Exception as e:
        print(f"[錯誤] 無法抓取 {job_id}: {e}")
        return None


async def test_hybrid_approach():
    """測試混合方案：Playwright 抓列表 + requests 抓詳情"""
    print("=" * 60)
    print("測試混合方案：Playwright (CDP) + requests")
    print("=" * 60)
    print()
    
    # 步驟 1: 使用 Playwright 抓取職缺 URL 列表
    job_urls = await get_job_urls_with_playwright("資料工程", max_jobs=5)
    
    if not job_urls:
        print("[失敗] 未能抓取到職缺 URL")
        return
    
    # 步驟 2: 使用 requests 抓取每個職缺的詳情
    print("========== 使用 requests 抓取職缺詳情 ==========\n")
    
    for i, job_url in enumerate(job_urls, 1):
        print(f"正在抓取職缺 {i}/{len(job_urls)}...")
        job_detail = get_job_detail_with_requests(job_url)
        
        if job_detail:
            print(f"[成功] {job_detail['title']}")
            print(f"  公司: {job_detail['company']}")
            print(f"  地點: {job_detail['location']}")
            print(f"  學歷: {job_detail['education']}")
            print(f"  經驗: {job_detail['experience']}")
            print(f"  薪資: {job_detail['salary']}")
            print(f"  工作內容: {job_detail['description']}")
            print()
        else:
            print(f"[失敗] 無法抓取職缺詳情")
            print()
    
    print("=" * 60)
    print("測試完成！混合方案可行！")
    print("=" * 60)


if __name__ == '__main__':
    print("\n提示：請確保 Chrome 已使用以下指令啟動：")
    print('chrome.exe --remote-debugging-port=9527 --user-data-dir="E:\\Chrome User Data"')
    print("\n開始測試...\n")
    
    asyncio.run(test_hybrid_approach())
