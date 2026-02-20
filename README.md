# 104 職缺爬蟲系統 - Portable 版本

## 🚀 3 步驟快速開始

### 步驟 1: 自動安裝環境
```bash
setup.bat
```
執行後會自動：
- 下載 Python 3.11.8
- 安裝所有依賴套件
- 安裝 Playwright 瀏覽器

**耗時**: 約 3-5 分鐘

### 步驟 2: 啟動 Chrome
```bash
start_chrome_cdp.bat
```

### 步驟 3: 執行爬蟲
```bash
run_scraper.bat
```

---

## 📋 檔案說明

### 執行檔
- **setup.bat** - 🌟 一鍵自動安裝環境（首次使用必執行）
- **start_chrome_cdp.bat** - 啟動 Chrome CDP
- **run_scraper.bat** - 執行爬蟲（手動模式）
- **run_scraper_schedule.bat** - 執行爬蟲（排程模式）
- **install_dependencies.bat** - 安裝依賴套件（手動方式）

### 說明文件
- **QUICK_START.md** - 快速開始指南 ⭐
- **README_PORTABLE.md** - 完整部署指南
- **DEPLOYMENT_SUMMARY.md** - 部署總結
- **PYTHON_SETUP.md** - Python 環境設置（手動方式）

### 程式碼
- **job_scraper_104/** - 爬蟲程式碼
- **data/** - 資料檔案（技術關鍵字、已抓取職缺）

---

## ⚙️ 必須調整的參數

### Chrome 路徑（重要！）
編輯 `start_chrome_cdp.bat`，修改為實際的 Chrome 安裝路徑：
```batch
"C:\Program Files\Google\Chrome\Application\chrome.exe"
```

### 搜尋關鍵字（可選）
編輯 `job_scraper_104\config.py`：
```python
KEYWORDS = ["資料工程", "資料分析", "RPA自動化"]
```

---

## 📊 系統資訊

- **Python 版本**: 3.11.8
- **套件依賴**: requests, schedule, PyYAML, playwright
- **作業系統**: Windows 10/11 (64-bit)
- **大小**: 約 0.45 MB（不含 Python 環境）

---

## 🆘 遇到問題？

1. 查看 `logs\scraper.log` 日誌檔案
2. 閱讀 `README_PORTABLE.md` 完整指南
3. 檢查 Chrome 是否已啟動（CDP 模式）

---

**版本**: 2.0.0 (Portable)  
**更新日期**: 2026-02-17
