"""
使用 Playwright 測試 104 職缺爬取
這個版本使用真實瀏覽器來避開反爬蟲機制
"""

import sys
import os
import asyncio

# 設定 UTF-8 編碼
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.async_api import async_playwright


async def test_104_with_playwright():
    """使用 Playwright 測試 104 職缺搜尋"""
    print("========== 使用 Playwright 測試 104 ==========\n")
    
    async with async_playwright() as p:
        # 啟動瀏覽器
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 1. 導航到搜尋頁面
            print("1. 正在導航到 104 搜尋頁面...")
            await page.goto('https://www.104.com.tw/jobs/search/?keyword=資料工程')
            await page.wait_for_load_state('networkidle')
            
            # 2. 等待職缺列表載入
            print("2. 等待職缺列表載入...")
            await page.wait_for_selector('article[data-job-no]', timeout=10000)
            
            # 3. 取得職缺列表
            jobs = await page.query_selector_all('article[data-job-no]')
            print(f"3. [成功] 找到 {len(jobs)} 個職缺\n")
            
            # 4. 顯示前 3 個職缺資訊
            for i, job in enumerate(jobs[:3], 1):
                job_id = await job.get_attribute('data-job-no')
                title_elem = await job.query_selector('a.js-job-link')
                title = await title_elem.inner_text() if title_elem else 'N/A'
                company_elem = await job.query_selector('[data-v-5e3c5f04]')
                company = await company_elem.inner_text() if company_elem else 'N/A'
                
                print(f"職缺 {i}:")
                print(f"  ID: {job_id}")
                print(f"  標題: {title.strip()}")
                print(f"  公司: {company.strip()}")
                print()
            
            # 5. 測試點擊進入職缺詳情
            if jobs:
                print("5. 測試點擊第一個職缺...")
                first_job_link = await jobs[0].query_selector('a.js-job-link')
                if first_job_link:
                    await first_job_link.click()
                    await page.wait_for_load_state('networkidle')
                    
                    # 等待工作內容載入
                    await page.wait_for_selector('.job-description', timeout=10000)
                    
                    # 取得工作內容
                    job_desc_elem = await page.query_selector('.job-description')
                    if job_desc_elem:
                        job_desc = await job_desc_elem.inner_text()
                        print(f"[成功] 工作內容長度: {len(job_desc)} 字元")
                        print(f"工作內容前 100 字: {job_desc[:100]}...")
                    
                    print("\n測試完成！Playwright 方案可行。")
                    
        except Exception as e:
            print(f"[錯誤] {e}")
        
        finally:
            await browser.close()


if __name__ == '__main__':
    asyncio.run(test_104_with_playwright())
