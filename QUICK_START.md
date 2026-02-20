# 🚀 快速開始指南（更新版）

## 📦 Portable 版本已準備完成！

**位置**: `D:\Users\User\Desktop\Side Project\网页自动化与API爬虫\python\104_Scraper_Portable\`

**大小**: 約 0.45 MB（不含 Python 環境）
**檔案數**: 195 個檔案

---

## ⚡ 3 分鐘快速部署（新版）

### 在其他電腦使用（全自動安裝）

```bash
# 1. 複製整個資料夾到新電腦

# 2. 執行自動安裝（一鍵完成所有設置）
setup.bat

# 3. 啟動 Chrome
start_chrome_cdp.bat

# 4. 執行爬蟲
run_scraper.bat
```

**setup.bat 會自動完成**：
- ✅ 下載 Python 3.11.8 Embeddable
- ✅ 解壓縮到 python\ 目錄
- ✅ 配置 Python 環境
- ✅ 安裝 pip
- ✅ 安裝所有依賴套件
- ✅ 安裝 Playwright 瀏覽器

**總耗時**: 約 3-5 分鐘（視網路速度）

---

### 在本機使用（已有 Python 環境）

```bash
# 1. 進入目錄
cd "D:\Users\User\Desktop\Side Project\网页自动化与API爬虫\python\104_Scraper_Portable"

# 2. 安裝依賴（使用現有 Python）
D:\miniconda3\envs\auto_env\python.exe -m pip install -r job_scraper_104\requirements_portable.txt

# 3. 啟動 Chrome
start_chrome_cdp.bat

# 4. 執行爬蟲
D:\miniconda3\envs\auto_env\python.exe job_scraper_104\main.py --mode manual
```

---

## 🔧 必須調整的參數（重要！）

### 1. Chrome 路徑

**檔案**: `start_chrome_cdp.bat`  
**第 23 行**: 修改為實際的 Chrome 安裝路徑

```batch
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ...
```

### 2. 搜尋關鍵字（可選）

**檔案**: `job_scraper_104\config.py`  
**第 9 行**:

```python
KEYWORDS = ["資料工程", "資料分析", "RPA自動化"]
```

### 3. 抓取數量（可選）

**檔案**: `job_scraper_104\config.py`  
**第 13 行**:

```python
MAX_JOBS_PER_KEYWORD = 50
```

---

## 🆕 新增檔案

- **setup.bat** - 🌟 一鍵自動安裝所有環境（新增）

---

## 📚 完整文件

- **QUICK_START.md** - 快速開始（本文件）
- **README_PORTABLE.md** - 完整部署指南
- **PYTHON_SETUP.md** - Python 環境設置（手動方式）
- **DEPLOYMENT_SUMMARY.md** - 部署總結

---

## ✅ 檢查清單

### 使用 setup.bat 自動安裝（推薦）

- [ ] 執行 `setup.bat`（自動完成所有設置）
- [ ] 調整 Chrome 路徑（`start_chrome_cdp.bat`）
- [ ] 啟動 Chrome（`start_chrome_cdp.bat`）
- [ ] 執行爬蟲（`run_scraper.bat`）

### 手動安裝

- [ ] 下載 Python Embeddable
- [ ] 解壓縮到 python\ 目錄
- [ ] 修改 python311._pth
- [ ] 安裝 pip
- [ ] 安裝依賴套件
- [ ] 調整 Chrome 路徑
- [ ] 啟動 Chrome
- [ ] 執行爬蟲

---

## 🎯 setup.bat 執行流程

```
步驟 1/6: 下載 Python Embeddable (約 30 秒)
步驟 2/6: 解壓縮 Python (約 10 秒)
步驟 3/6: 配置 Python 環境 (約 5 秒)
步驟 4/6: 安裝 pip (約 20 秒)
步驟 5/6: 安裝 Python 套件 (約 1-2 分鐘)
步驟 6/6: 安裝 Playwright 瀏覽器 (約 1-2 分鐘)
```

**總耗時**: 約 3-5 分鐘

---

**準備時間**: 約 3-5 分鐘（使用 setup.bat）  
**首次執行**: 約 7 分鐘（抓取 150 筆職缺）
