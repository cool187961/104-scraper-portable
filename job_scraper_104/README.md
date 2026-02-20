# 104 人力銀行職缺爬蟲系統 - 使用說明（混合方案版本）

## 🎯 混合方案架構

本系統採用 **Playwright CDP + requests** 混合方案：

1. **Playwright CDP** - 連接到已開啟的 Chrome 瀏覽器，抓取職缺 ID 列表
2. **requests** - 使用 HTTP 請求獲取每個職缺的詳細資訊

這種方案結合了兩者的優點：
- ✅ 繞過 104 的反爬蟲機制（使用真實瀏覽器）
- ✅ 快速獲取詳情（使用 API 請求）
- ✅ 資源消耗適中

## 📋 使用前準備

### 1. 啟動 Chrome（CDP 模式）

**方式一：使用批次檔（推薦）**
```bash
.\python\job_scraper_104\start_chrome_cdp.bat
```

**方式二：手動啟動**
```bash
chrome.exe --remote-debugging-port=9527 --user-data-dir="E:\Chrome User Data"
```

**重要提示**：
- 端口號必須是 `9527`（或修改 `scraper.py` 中的 `cdp_url`）
- `user-data-dir` 路徑可自訂，但必須是獨立的目錄
- 啟動後請保持 Chrome 視窗開啟

### 2. 確認環境

```bash
# 確認 Python 環境
D:\miniconda3\envs\auto_env\python.exe --version

# 確認套件已安裝
pip list | findstr "playwright requests schedule PyYAML"
```

## 🚀 使用方式

### 方式一：測試模式（推薦先測試）

```bash
cd "d:\Users\User\Desktop\Side Project\网页自动化与API爬虫"
D:\miniconda3\envs\auto_env\python.exe python\job_scraper_104\test_full_scraper.py
```

測試模式會：
- 只抓取「資料工程」3 筆職缺
- 顯示抓取結果
- 儲存為 Obsidian 筆記

### 方式二：完整執行（手動模式）

```bash
D:\miniconda3\envs\auto_env\python.exe python\job_scraper_104\main.py --mode manual
```

完整執行會：
- 抓取所有關鍵字（資料工程、資料分析、RPA自動化）
- 每個關鍵字抓取 50 筆（可在 `config.py` 調整）
- 自動儲存為 Obsidian 筆記

### 方式三：排程模式（定時執行）

```bash
D:\miniconda3\envs\auto_env\python.exe python\job_scraper_104\main.py --mode schedule
```

排程模式會：
- 每天早上 8:00 自動執行（可在 `config.py` 調整）
- 持續運行，按 `Ctrl+C` 停止

## ⚙️ 配置選項

編輯 `python/job_scraper_104/config.py`：

```python
# 搜尋關鍵字
KEYWORDS = ["資料工程", "資料分析", "RPA自動化"]

# 每個關鍵字抓取的職缺數
MAX_JOBS_PER_KEYWORD = 50

# 排序方式："date" (最近更新) 或 "relevance" (相關性)
SORT_BY = "date"

# 排程時間
SCHEDULE_TIME = "08:00"

# 延遲時間（避免請求過快）
REQUEST_DELAY_LIST = (3, 5)      # 列表頁延遲 3-5 秒
REQUEST_DELAY_DETAIL = (1, 3)    # 詳情頁延遲 1-3 秒

# 去重設定
ENABLE_DEDUPLICATION = True
```

## 📁 輸出結構

```
python/data/jobs/
├── 資料工程/
│   ├── 資料工程師_ABC公司_8lhbs.md
│   ├── 數據工程師_XYZ科技_7t6fy.md
│   └── ...
├── 資料分析/
│   └── ...
└── RPA自動化/
    └── ...
```

每個 Markdown 檔案包含：
- YAML frontmatter（標題、公司、薪資、地點、關鍵字、抓取時間、URL）
- 工作內容（已加上技術名詞雙向連結）
- 條件要求（學歷、經驗、技能、擅長工具、其他條件）

## 🔧 常見問題

### Q: CDP 連接失敗怎麼辦？

**錯誤訊息**：`connect_over_cdp: timeout`

**解決方法**：
1. 確認 Chrome 已使用 CDP 模式啟動
2. 確認端口號是 9527
3. 嘗試重新啟動 Chrome

### Q: 抓取到的職缺數量不足怎麼辦？

**原因**：頁面上可見的職缺數量有限

**解決方法**：
1. 在 Chrome 中手動滾動頁面載入更多職缺
2. 增加 `scraper.py` 中的頁面等待時間
3. 增加翻頁次數（修改 `page > 10` 的限制）

### Q: 如何修改 CDP 端口？

編輯 `scraper.py`：
```python
scraper = JobScraper(use_cdp=True, cdp_url="http://localhost:您的端口")
```

同時修改啟動 Chrome 的指令：
```bash
chrome.exe --remote-debugging-port=您的端口 --user-data-dir="路徑"
```

### Q: 如何關閉去重功能？

編輯 `config.py`：
```python
ENABLE_DEDUPLICATION = False
```

## 📊 技術細節

### CDP 連接流程

1. Chrome 以 CDP 模式啟動，監聽 9527 端口
2. Playwright 連接到 CDP 端點
3. 使用現有的瀏覽器 context 和 page
4. 執行 JavaScript 提取職缺 ID

### 職缺 ID 提取方法

從頁面連結中提取職缺 ID，支援兩種格式：
- 重定向格式：`job%2F8lhbs`
- 直接格式：`/job/8lhbs`

### API 請求

使用 requests 請求 104 的內部 API：
```
https://www.104.com.tw/job/ajax/content/{job_id}
```

返回 JSON 格式的職缺詳情。

## 🎓 進階使用

### 自訂技術關鍵字

編輯 `python/data/tech_keywords.yaml` 新增您的技術名詞。

### 審核自動學習的關鍵字

系統會自動從「擅長工具」欄位學習新技術名詞，儲存於 `python/data/learned_keywords.yaml`。您可隨時編輯此檔案。

### 在 Obsidian 中使用

1. 打開 Obsidian
2. 將 `python/data/jobs` 資料夾加入 Vault
3. 點擊任一技術名詞（如 `[[Python]]`）即可查看所有相關職缺

## 📝 日誌

所有執行紀錄儲存至 `python/logs/scraper.log`。

## ⚠️ 注意事項

1. **請勿過度頻繁執行**，建議每天執行 1-2 次
2. **遵守 104 使用條款**，僅供個人學習研究使用
3. **Chrome 必須保持開啟**，CDP 連接才能正常運作
4. **Cookie 可能過期**，如遇問題請重新登入 104 網站

---

**版本**: 2.0.0 (混合方案)  
**更新日期**: 2026-02-17
