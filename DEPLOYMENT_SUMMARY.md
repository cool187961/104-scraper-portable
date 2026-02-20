# 104 職缺爬蟲系統 - Portable 版本部署總結

## ✅ 已完成的工作

### 📦 Portable 資料夾結構

已建立完整的 Portable 版本於：
```
D:\Users\User\Desktop\Side Project\网页自动化与API爬虫\python\104_Scraper_Portable\
```

**包含內容**：
- ✅ 完整的爬蟲程式碼（`job_scraper_104/`）
- ✅ 資料檔案（`data/`）
- ✅ 批次執行檔（`.bat`）
- ✅ 說明文件（`.md`）

### 📝 建立的檔案

1. **README_PORTABLE.md** - 完整部署指南
2. **PYTHON_SETUP.md** - Python 環境設置說明
3. **install_dependencies.bat** - 依賴套件安裝腳本
4. **start_chrome_cdp.bat** - Chrome CDP 啟動腳本
5. **run_scraper.bat** - 執行爬蟲（手動模式）
6. **run_scraper_schedule.bat** - 執行爬蟲（排程模式）
7. **requirements_portable.txt** - 精簡版依賴清單

---

## 🔧 必須調整的參數

### 1. Chrome 路徑（最重要！）

**檔案**: `start_chrome_cdp.bat`

**預設路徑**:
```batch
"C:\Program Files\Google\Chrome\Application\chrome.exe"
```

**如果 Chrome 安裝在其他位置，請修改為**:
```batch
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
```
或其他實際路徑。

### 2. 搜尋關鍵字（可選）

**檔案**: `job_scraper_104\config.py`

**預設值**:
```python
KEYWORDS = ["資料工程", "資料分析", "RPA自動化"]
```

**可修改為**:
```python
KEYWORDS = ["Python工程師", "後端工程師", "全端工程師"]
```

### 3. 抓取數量（可選）

**檔案**: `job_scraper_104\config.py`

**預設值**:
```python
MAX_JOBS_PER_KEYWORD = 50
```

**可修改為**:
```python
MAX_JOBS_PER_KEYWORD = 10  # 測試用
MAX_JOBS_PER_KEYWORD = 100 # 大量抓取
```

### 4. 排程時間（可選）

**檔案**: `job_scraper_104\config.py`

**預設值**:
```python
SCHEDULE_TIME = "08:00"  # 早上 8:00
```

**可修改為**:
```python
SCHEDULE_TIME = "14:30"  # 下午 2:30
SCHEDULE_TIME = "20:00"  # 晚上 8:00
```

### 5. 輸出目錄（可選）

**檔案**: `job_scraper_104\config.py`

**預設值**（相對路徑）:
```python
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "jobs")
```

**可修改為絕對路徑**:
```python
OUTPUT_DIR = r"D:\我的Obsidian\職缺筆記"
```

---

## 🚀 在其他電腦使用的步驟

### 步驟 1: 複製整個資料夾

將 `104_Scraper_Portable` 資料夾複製到新電腦的任意位置。

### 步驟 2: 設置 Python 環境

**選擇以下方式之一**：

#### 方式 A: 使用 Python Embeddable（推薦）

1. 下載 Python 3.11 Embeddable:
   https://www.python.org/ftp/python/3.11.8/python-3.11.8-embed-amd64.zip

2. 解壓縮到 `104_Scraper_Portable\python\`

3. 修改 `python\python311._pth`，取消註解 `import site`

4. 下載並執行 get-pip.py:
   ```bash
   python\python.exe get-pip.py
   ```

5. 執行 `install_dependencies.bat`

#### 方式 B: 使用虛擬環境

```bash
cd 104_Scraper_Portable
python -m venv python
python\Scripts\activate
pip install -r job_scraper_104\requirements_portable.txt
```

### 步驟 3: 調整參數

根據新電腦的環境，調整以下參數：
- Chrome 路徑（`start_chrome_cdp.bat`）
- 輸出目錄（`job_scraper_104\config.py`）

### 步驟 4: 執行爬蟲

1. 執行 `start_chrome_cdp.bat`（啟動 Chrome）
2. 執行 `run_scraper.bat`（開始爬取）

---

## 📊 套件版本清單

根據 `auto_env` 環境的實際版本：

```
requests==2.32.5
schedule==1.2.2
PyYAML==6.0.3
playwright==1.58.0
```

**總大小估計**: 約 50-100 MB（含 Playwright 瀏覽器）

---

## ⚠️ 重要注意事項

### 1. Python 環境

由於 Python 環境較大（100-200MB），未包含在 Portable 資料夾中。
請依照 `PYTHON_SETUP.md` 的說明建立 Python 環境。

### 2. Chrome 瀏覽器

新電腦必須安裝 Chrome 瀏覽器，且需要調整 `start_chrome_cdp.bat` 中的路徑。

### 3. 網路連線

爬蟲需要網路連線才能運作。

### 4. 防火牆設定

某些防火牆可能會阻擋 CDP 連接（端口 9527），請允許連線。

---

## 📁 資料夾內容

```
104_Scraper_Portable/
├── job_scraper_104/          # 爬蟲程式碼（25 個檔案）
├── data/                     # 資料檔案（162 個檔案）
│   ├── tech_keywords.yaml
│   ├── learned_keywords.yaml
│   └── jobs/
│       ├── 資料工程/（52 個筆記）
│       ├── 資料分析/（50 個筆記）
│       └── RPA自動化/（50 個筆記）
├── python/                   # Python 環境（需自行建立）
├── *.bat                     # 批次執行檔（4 個）
└── *.md                      # 說明文件（3 個）
```

**總檔案數**: 約 250 個檔案
**總大小**: 約 5-10 MB（不含 Python 環境）

---

## ✅ 檢查清單

在新電腦使用前，請確認：

- [ ] 已複製整個 `104_Scraper_Portable` 資料夾
- [ ] 已建立 Python 環境（`python\python.exe` 存在）
- [ ] 已安裝依賴套件（執行 `install_dependencies.bat`）
- [ ] 已安裝 Chrome 瀏覽器
- [ ] 已調整 Chrome 路徑（`start_chrome_cdp.bat`）
- [ ] 已調整輸出目錄（如需要）
- [ ] 已調整搜尋關鍵字（如需要）
- [ ] 網路連線正常

---

**建立日期**: 2026-02-17  
**版本**: 2.0.0 (Portable)  
**適用系統**: Windows 10/11 (64-bit)
