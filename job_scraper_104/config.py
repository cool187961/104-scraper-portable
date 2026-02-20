"""
配置管理模組
所有參數均可由用戶自訂
"""

import os

# ==================== 搜尋關鍵字 ====================
KEYWORDS = ["資料工程", "資料分析", "RPA自動化","AI應用"]

# ==================== 職缺數量設定 ====================
# 每個關鍵字抓取的最大職缺數（預設 50，可調整）
MAX_JOBS_PER_KEYWORD = 50

# ==================== 排序設定 ====================
# 職缺排序方式："date" (最近更新) 或 "relevance" (相關性)
SORT_BY = "relevance"  # 預設為「最近更新」

# ==================== Rate Limiting ====================
# 請求延遲時間（秒），使用隨機範圍避免被偵測
REQUEST_DELAY_LIST = (3, 5)      # 列表頁延遲 3-5 秒
REQUEST_DELAY_DETAIL = (1, 3)    # 詳情頁延遲 1-3 秒

# ==================== 路徑設定 ====================
# 取得專案根目錄（python 資料夾）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Obsidian 筆記輸出路徑
OUTPUT_DIR = r'C:\ObsidianVault\MyKnowledgeBase\jobs'

# 技術關鍵字檔案路徑
KEYWORDS_FILE = os.path.join(BASE_DIR, "data", "tech_keywords.yaml")
LEARNED_KEYWORDS_FILE = os.path.join(BASE_DIR, "data", "learned_keywords.yaml")

# ==================== 排程設定 ====================
# 排程時間（預設早上 8:00，可調整）
SCHEDULE_TIME = "08:00"

# ==================== 去重設定 ====================
# 是否啟用職缺去重機制
ENABLE_DEDUPLICATION = True

# ==================== API 設定 ====================
# 104 人力銀行 API 端點
API_BASE_URL = "https://www.104.com.tw"
API_SEARCH_ENDPOINT = "/jobs/search/list"
API_JOB_DETAIL_ENDPOINT = "/job/ajax/content"

# ==================== 日誌設定 ====================
# 日誌檔案路徑
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "scraper.log")

# 確保日誌目錄存在
os.makedirs(LOG_DIR, exist_ok=True)
