"""
測試 API 客戶端功能
驗證職缺搜尋與詳情查詢是否正常運作
"""

import sys
import os

# 設定 UTF-8 編碼（解決 Windows 終端機編碼問題）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_scraper_104.api_client import Job104APIClient
from job_scraper_104 import config


def test_search_jobs():
    """測試職缺搜尋功能"""
    print("========== 測試職缺搜尋功能 ==========")
    
    client = Job104APIClient()
    
    # 測試搜尋「資料工程」
    result = client.search_jobs(keyword="資料工程", page=1, sort_by="date")
    
    if result:
        jobs = result.get('data', {}).get('list', [])
        print(f"[成功] 搜尋成功，取得 {len(jobs)} 筆職缺")
        
        if jobs:
            print(f"第一筆職缺：{jobs[0].get('jobName', 'N/A')}")
            return jobs[0].get('jobNo', None)
    else:
        print("[失敗] 搜尋失敗")
        return None
    
    client.close()


def test_get_job_detail(job_id: str):
    """測試職缺詳情查詢功能"""
    if not job_id:
        print("跳過詳情測試（無有效 job_id）")
        return
    
    print(f"\n========== 測試職缺詳情查詢功能 (job_id={job_id}) ==========")
    
    client = Job104APIClient()
    result = client.get_job_detail(job_id)
    
    if result and 'data' in result:
        print("[成功] 取得職缺詳情成功")
        
        # 顯示部分資訊
        detail = result['data'].get('jobDetail', {})
        print(f"工作內容長度：{len(detail.get('jobDescription', ''))} 字元")
        print(f"工作地點：{detail.get('addressRegion', 'N/A')}{detail.get('addressDetail', '')}")
    else:
        print("[失敗] 取得職缺詳情失敗")
    
    client.close()


if __name__ == '__main__':
    job_id = test_search_jobs()
    test_get_job_detail(job_id)
    
    print("\n測試完成！")
