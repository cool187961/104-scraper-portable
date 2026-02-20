"""
改進版 CDP 測試：處理動態載入和滾動
"""

import sys
import os
import asyncio
import re

# 設定 UTF-8 編碼
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.async_api import async_playwright
import requests


async def get_job_ids_from_cdp(keyword: str = "資料工程", max_jobs: int = 5):
    """從 CDP 連接的 Chrome 獲取職缺 ID"""
    async with async_playwright() as p:
        try:
            print("1. 連接到 Chrome (CDP)...")
            browser = await p.chromium.connect_over_cdp("http://localhost:9527")
            
            context = browser.contexts[0]
            page = context.pages[0]
            
            print(f"2. 當前 URL: {page.url}\n")
            
            # 導航到搜尋頁面
            search_url = f"https://www.104.com.tw/jobs/search/?keyword={keyword}"
            print(f"3. 導航到: {search_url}")
            await page.goto(search_url, wait_until='domcontentloaded')
            
            # 等待並滾動頁面
            print("4. 等待頁面載入並滾動...")
            await asyncio.sleep(5)
            
            # 滾動頁面以觸發懶載入
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            await asyncio.sleep(2)
            
            # 嘗試多種方法獲取職缺 ID
            print("\n5. 嘗試獲取職缺 ID...\n")
            
            # 方法1: 從 article 元素獲取
            job_ids_method1 = await page.evaluate("""
                () => {
                    const articles = document.querySelectorAll('article[data-job-no]');
                    console.log('Found articles:', articles.length);
                    return Array.from(articles).map(a => a.getAttribute('data-job-no')).filter(id => id);
                }
            """)
            print(f"   方法1 (article[data-job-no]): 找到 {len(job_ids_method1)} 個")
            
            # 方法2: 從連結 href 提取
            job_ids_method2 = await page.evaluate("""
                () => {
                    const links = document.querySelectorAll('a[href*="/job/"]');
                    console.log('Found links:', links.length);
                    const ids = [];
                    links.forEach(link => {
                        const href = link.getAttribute('href');
                        const match = href.match(/\\/job\\/([a-z0-9]+)/);
                        if (match && match[1]) {
                            ids.push(match[1]);
                        }
                    });
                    return [...new Set(ids)]; // 去重
                }
            """)
            print(f"   方法2 (a[href*=\"/job/\"]): 找到 {len(job_ids_method2)} 個")
            
            # 方法3: 從所有連結中提取（包括重定向連結）
            job_ids_method3 = await page.evaluate("""
                () => {
                    const links = document.querySelectorAll('a[href]');
                    console.log('Total links:', links.length);
                    const ids = [];
                    links.forEach(link => {
                        const href = link.getAttribute('href');
                        // 匹配 job%2F8lhbs 格式
                        let match = href.match(/job%2F([a-z0-9]+)/);
                        if (match && match[1]) {
                            ids.push(match[1]);
                        } else {
                            // 匹配 /job/8lhbs 格式
                            match = href.match(/\\/job\\/([a-z0-9]+)/);
                            if (match && match[1]) {
                                ids.push(match[1]);
                            }
                        }
                    });
                    return [...new Set(ids)]; // 去重
                }
            """)
            print(f"   方法3 (所有連結): 找到 {len(job_ids_method3)} 個")
            
            # 選擇找到最多的方法
            job_ids = job_ids_method3 if len(job_ids_method3) > 0 else (job_ids_method2 if len(job_ids_method2) > 0 else job_ids_method1)
            
            if job_ids:
                print(f"\n✓ 成功找到 {len(job_ids)} 個職缺 ID")
                print("\n前 10 個職缺 ID:")
                for i, job_id in enumerate(job_ids[:10], 1):
                    print(f"  {i}. {job_id}")
                
                return job_ids[:max_jobs]
            else:
                print("\n✗ 未找到任何職缺 ID")
                return []
            
        except Exception as e:
            print(f"錯誤: {e}")
            import traceback
            traceback.print_exc()
            return []


def fetch_job_detail(job_id: str):
    """使用 requests 獲取職缺詳情"""
    api_url = f"https://www.104.com.tw/job/ajax/content/{job_id}"
    job_url = f"https://www.104.com.tw/job/{job_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': job_url,
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'data' in data:
            job_detail = data['data'].get('jobDetail', {})
            condition = data['data'].get('condition', {})
            
            return {
                'job_id': job_id,
                'title': job_detail.get('jobName', 'N/A'),
                'company': job_detail.get('custName', 'N/A'),
                'location': f"{job_detail.get('addressRegion', '')}{job_detail.get('addressDetail', '')}",
                'salary': job_detail.get('salary', 'N/A'),
                'education': condition.get('edu', 'N/A'),
                'experience': condition.get('workExp', 'N/A'),
            }
        return None
        
    except Exception as e:
        print(f"  [錯誤] {job_id}: {e}")
        return None


async def main():
    print("=" * 70)
    print("混合方案測試：Playwright CDP (抓列表) + requests (抓詳情)")
    print("=" * 70)
    print()
    
    # 步驟1: 使用 Playwright CDP 獲取職缺 ID
    job_ids = await get_job_ids_from_cdp("資料工程", max_jobs=5)
    
    if not job_ids:
        print("\n[失敗] 無法獲取職缺 ID")
        return
    
    # 步驟2: 使用 requests 獲取詳情
    print("\n" + "=" * 70)
    print("使用 requests 獲取職缺詳情")
    print("=" * 70)
    print()
    
    for i, job_id in enumerate(job_ids, 1):
        print(f"[{i}/{len(job_ids)}] 正在抓取 {job_id}...")
        detail = fetch_job_detail(job_id)
        
        if detail:
            print(f"  ✓ {detail['title']}")
            print(f"    公司: {detail['company']}")
            print(f"    地點: {detail['location']}")
            print(f"    薪資: {detail['salary']}")
            print(f"    學歷: {detail['education']}")
            print(f"    經驗: {detail['experience']}")
        print()
    
    print("=" * 70)
    print("測試完成！")
    print("=" * 70)


if __name__ == '__main__':
    asyncio.run(main())
