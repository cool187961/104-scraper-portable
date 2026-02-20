# 104 職缺爬蟲系統 - Portable 版本部署指南

## 📦 Portable 版本說明

此為 104 職缺爬蟲系統的可攜式版本，可在任何 Windows 電腦上運行，無需安裝 Python 環境。

---

## 📋 系統需求

- **作業系統**: Windows 10/11 (64-bit)
- **硬碟空間**: 至少 500MB
- **網路**: 需要網路連線
- **Chrome 瀏覽器**: 必須安裝（用於 CDP 連接）

---

## 🚀 快速開始

### 步驟 1: 解壓縮

將整個資料夾解壓縮到任意位置，例如：
```
D:\104_Scraper_Portable\
```

### 步驟 2: 安裝 Python 依賴（首次使用）

執行以下指令安裝必要套件：

```bash
cd D:\104_Scraper_Portable
python\python.exe -m pip install -r job_scraper_104\requirements_portable.txt
```

或使用提供的批次檔：
```bash
install_dependencies.bat
```

### 步驟 3: 安裝 Playwright 瀏覽器（首次使用）

```bash
python\python.exe -m playwright install chromium
```

### 步驟 4: 啟動 Chrome CDP

執行批次檔：
```bash
start_chrome_cdp.bat
```

或手動執行：
```bash
chrome.exe --remote-debugging-port=9527 --user-data-dir=".\chrome_user_data"
```

### 步驟 5: 執行爬蟲

**手動模式**（立即執行）：
```bash
run_scraper.bat
```

**排程模式**（定時執行）：
```bash
run_scraper_schedule.bat
```

---

## ⚙️ 必須調整的參數

### 1. Chrome CDP 路徑（如果 Chrome 不在預設位置）

編輯 `start_chrome_cdp.bat`：
```batch
REM 修改 Chrome 執行檔路徑
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9527 --user-data-dir="%~dp0chrome_user_data"
```

### 2. 輸出目錄（可選）

編輯 `job_scraper_104\config.py`：
```python
# 修改輸出目錄為絕對路徑或相對路徑
OUTPUT_DIR = r"D:\我的職缺筆記"  # 絕對路徑
# 或
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "jobs")  # 相對路徑（預設）
```

### 3. 搜尋關鍵字（可選）

編輯 `job_scraper_104\config.py`：
```python
# 修改搜尋關鍵字
KEYWORDS = ["資料工程", "資料分析", "RPA自動化", "Python工程師"]  # 可自訂
```

### 4. 抓取數量（可選）

編輯 `job_scraper_104\config.py`：
```python
# 修改每個關鍵字抓取的職缺數量
MAX_JOBS_PER_KEYWORD = 50  # 預設 50，可調整為 10, 20, 100 等
```

### 5. 排程時間（可選）

編輯 `job_scraper_104\config.py`：
```python
# 修改排程時間（24 小時制）
SCHEDULE_TIME = "08:00"  # 預設早上 8:00，可改為 "14:30", "20:00" 等
```

---

## 📁 資料夾結構

```
104_Scraper_Portable/
├── python/                          # Portable Python 環境
│   ├── python.exe                   # Python 執行檔
│   ├── Lib/                         # Python 標準庫
│   └── Scripts/                     # Python 腳本
├── job_scraper_104/                 # 爬蟲程式碼
│   ├── __init__.py
│   ├── api_client.py                # API 客戶端
│   ├── config.py                    # 配置檔案 ⚙️
│   ├── scraper.py                   # 爬蟲主程式
│   ├── keyword_linker.py            # 技術名詞連結
│   ├── obsidian_formatter.py        # Obsidian 格式化
│   ├── scheduler.py                 # 排程管理
│   ├── main.py                      # 主程式入口
│   └── requirements_portable.txt    # 依賴套件清單
├── data/                            # 資料目錄
│   ├── tech_keywords.yaml           # 預定義技術關鍵字
│   ├── learned_keywords.yaml        # 自動學習的關鍵字
│   └── jobs/                        # Obsidian 筆記輸出
│       ├── 資料工程/
│       ├── 資料分析/
│       └── RPA自動化/
├── logs/                            # 日誌目錄
│   └── scraper.log                  # 執行日誌
├── chrome_user_data/                # Chrome 用戶資料（自動建立）
├── install_dependencies.bat         # 安裝依賴批次檔
├── start_chrome_cdp.bat             # 啟動 Chrome CDP
├── run_scraper.bat                  # 執行爬蟲（手動模式）
├── run_scraper_schedule.bat         # 執行爬蟲（排程模式）
└── README_PORTABLE.md               # 本說明文件
```

---

## 🔧 常見問題

### Q1: 找不到 Python？

**解決方法**：
1. 確認 `python` 資料夾存在
2. 檢查 `python\python.exe` 是否存在
3. 使用絕對路徑執行

### Q2: CDP 連接失敗？

**錯誤訊息**: `connect_over_cdp: timeout`

**解決方法**：
1. 確認 Chrome 已使用 CDP 模式啟動
2. 檢查端口 9527 是否被占用
3. 嘗試重新啟動 Chrome

### Q3: 套件安裝失敗？

**解決方法**：
1. 確認網路連線正常
2. 使用管理員權限執行
3. 手動安裝：
   ```bash
   python\python.exe -m pip install requests==2.32.5
   python\python.exe -m pip install schedule==1.2.2
   python\python.exe -m pip install PyYAML==6.0.3
   python\python.exe -m pip install playwright==1.58.0
   ```

### Q4: 如何在其他電腦使用？

**步驟**：
1. 複製整個 `104_Scraper_Portable` 資料夾到新電腦
2. 確認新電腦已安裝 Chrome
3. 執行 `install_dependencies.bat`（如果 Python 環境不完整）
4. 執行 `start_chrome_cdp.bat`
5. 執行 `run_scraper.bat`

### Q5: 如何更新爬蟲程式？

**步驟**：
1. 備份 `data` 資料夾（保留已抓取的職缺）
2. 備份 `job_scraper_104\config.py`（保留自訂設定）
3. 下載新版本並覆蓋 `job_scraper_104` 資料夾
4. 還原 `config.py` 和 `data` 資料夾

---

## 📝 使用注意事項

1. **Chrome 必須保持開啟**: CDP 連接需要 Chrome 運行
2. **首次執行較慢**: 需要載入瀏覽器和安裝套件
3. **網路連線**: 抓取職缺需要網路
4. **遵守使用條款**: 僅供個人學習研究使用
5. **適度使用**: 建議每天執行 1-2 次

---

## 📊 效能參考

- **抓取速度**: 約 2-3 秒/職缺
- **記憶體使用**: 約 200-300 MB
- **硬碟空間**: 每 100 筆職缺約 500 KB

---

## 🆘 技術支援

如遇問題，請檢查：
1. `logs\scraper.log` - 執行日誌
2. Chrome 開發者工具（F12）- 網頁錯誤
3. Windows 事件檢視器 - 系統錯誤

---

**版本**: 2.0.0 (Portable)  
**更新日期**: 2026-02-17  
**Python 版本**: 3.11.x
