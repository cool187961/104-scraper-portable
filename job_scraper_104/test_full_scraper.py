"""
測試完整爬蟲系統（混合方案）
"""

import sys
import os

# 設定 UTF-8 編碼
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_scraper_104.scraper import JobScraper
from job_scraper_104 import config


def test_full_scraper():
    """測試完整爬蟲系統"""
    print("=" * 70)
    print("測試完整爬蟲系統（混合方案：CDP + requests）")
    print("=" * 70)
    print()
    
    print("配置資訊:")
    print(f"  關鍵字: {config.KEYWORDS}")
    print(f"  每個關鍵字抓取數量: {config.MAX_JOBS_PER_KEYWORD}")
    print(f"  排序方式: {config.SORT_BY}")
    print(f"  輸出目錄: {config.OUTPUT_DIR}")
    print(f"  去重: {'啟用' if config.ENABLE_DEDUPLICATION else '停用'}")
    print()
    
    print("提示：請確保 Chrome 已使用以下指令啟動：")
    print('chrome.exe --remote-debugging-port=9527 --user-data-dir="E:\\Chrome User Data"')
    print()
    
    input("按 Enter 開始測試...")
    print()
    
    try:
        # 初始化爬蟲（使用 CDP）
        scraper = JobScraper(use_cdp=True, cdp_url="http://localhost:9527")
        
        # 測試單一關鍵字（只抓 3 筆）
        print("測試模式：只抓取「資料工程」3 筆職缺\n")
        
        jobs = scraper.scrape_keyword("資料工程", max_jobs=3)
        
        print("\n" + "=" * 70)
        print(f"成功抓取 {len(jobs)} 筆職缺")
        print("=" * 70)
        print()
        
        # 顯示結果
        for i, job in enumerate(jobs, 1):
            print(f"職缺 {i}:")
            print(f"  標題: {job['title']}")
            print(f"  公司: {job['company']}")
            print(f"  地點: {job['location']}")
            print(f"  薪資: {job['salary']}")
            print(f"  學歷: {job['education']}")
            print(f"  經驗: {job['experience']}")
            print(f"  擅長工具: {', '.join(job['specialty'][:5]) if job['specialty'] else '無'}")
            print()
        
        # 儲存為 Obsidian 筆記
        print("正在儲存為 Obsidian 筆記...")
        for job in jobs:
            scraper.formatter.save_job_note(job, "資料工程")
        
        print(f"\n✓ 筆記已儲存至: {config.OUTPUT_DIR}/資料工程/")
        print()
        
        print("=" * 70)
        print("測試完成！")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n[錯誤] {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_full_scraper()
