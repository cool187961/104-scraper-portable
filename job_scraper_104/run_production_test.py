"""
正式執行腳本 - 測試完整功能與去重機制
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


def main():
    """執行正式爬蟲測試"""
    print("=" * 80)
    print("104 職缺爬蟲系統 - 正式執行測試")
    print("=" * 80)
    print()
    
    print("📋 配置資訊:")
    print(f"  關鍵字: {config.KEYWORDS}")
    print(f"  每個關鍵字抓取數量: 10 筆（測試用）")
    print(f"  去重: {'啟用' if config.ENABLE_DEDUPLICATION else '停用'}")
    print(f"  輸出目錄: {config.OUTPUT_DIR}")
    print()
    
    print("⚠️  提示：請確保 Chrome 已使用 CDP 模式啟動")
    print("   chrome.exe --remote-debugging-port=9527 --user-data-dir=\"E:\\Chrome User Data\"")
    print()
    
    input("按 Enter 開始執行...")
    print()
    
    try:
        # 初始化爬蟲
        scraper = JobScraper(use_cdp=True, cdp_url="http://localhost:9527")
        
        # 只測試「資料工程」類別，抓取 10 筆
        keyword = "資料工程"
        max_jobs = 10
        
        print(f"🚀 開始抓取「{keyword}」職缺（目標：{max_jobs} 筆）")
        print("=" * 80)
        print()
        
        jobs = scraper.scrape_keyword(keyword, max_jobs=max_jobs)
        
        print()
        print("=" * 80)
        print(f"✅ 抓取完成！共取得 {len(jobs)} 筆職缺")
        print("=" * 80)
        print()
        
        # 顯示統計資訊
        print("📊 統計資訊:")
        print(f"  總職缺數: {len(jobs)}")
        print(f"  去重後數量: {len(scraper.scraped_job_ids)}")
        print(f"  已抓取 ID: {', '.join(list(scraper.scraped_job_ids)[:10])}...")
        print()
        
        # 顯示前 5 筆職缺摘要
        print("📝 前 5 筆職缺摘要:")
        print("-" * 80)
        for i, job in enumerate(jobs[:5], 1):
            print(f"\n{i}. {job['title']}")
            print(f"   公司: {job['company']}")
            print(f"   地點: {job['location']}")
            print(f"   薪資: {job['salary']}")
            print(f"   學歷: {job['education']} | 經驗: {job['experience']}")
            
            # 顯示擅長工具
            if job['specialty']:
                print(f"   擅長工具: {', '.join(job['specialty'][:5])}")
                if len(job['specialty']) > 5:
                    print(f"             ... 等共 {len(job['specialty'])} 項")
            
            # 顯示工作內容前 100 字
            desc = job['job_description'].replace('\n', ' ').strip()
            if desc:
                print(f"   工作內容: {desc[:100]}...")
        
        print()
        print("-" * 80)
        
        # 儲存為 Obsidian 筆記
        print()
        print("💾 正在儲存為 Obsidian 筆記...")
        saved_count = 0
        for job in jobs:
            scraper.formatter.save_job_note(job, keyword)
            saved_count += 1
        
        print(f"✅ 已儲存 {saved_count} 個筆記至: {config.OUTPUT_DIR}/{keyword}/")
        print()
        
        # 測試去重機制
        print("=" * 80)
        print("🔍 測試去重機制")
        print("=" * 80)
        print()
        print("再次執行相同的抓取，應該會跳過已抓取的職缺...")
        print()
        
        # 記錄已抓取的 ID
        before_ids = scraper.scraped_job_ids.copy()
        print(f"第一次抓取的 ID 數量: {len(before_ids)}")
        
        # 再次抓取（應該會去重）
        jobs_2 = scraper.scrape_keyword(keyword, max_jobs=5)
        
        after_ids = scraper.scraped_job_ids
        new_ids = after_ids - before_ids
        
        print(f"第二次抓取後的 ID 數量: {len(after_ids)}")
        print(f"新增的 ID 數量: {len(new_ids)}")
        
        if len(new_ids) > 0:
            print(f"新增的 ID: {', '.join(new_ids)}")
        else:
            print("✅ 去重機制正常運作！沒有重複抓取")
        
        print()
        print("=" * 80)
        print("🎉 測試完成！")
        print("=" * 80)
        print()
        print(f"📁 請查看生成的筆記: {config.OUTPUT_DIR}/{keyword}/")
        print()
        
    except Exception as e:
        print()
        print("=" * 80)
        print(f"❌ 錯誤: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
