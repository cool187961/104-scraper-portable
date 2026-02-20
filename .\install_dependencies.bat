@echo off
chcp 65001 >nul
echo ========================================
echo 安裝 104 爬蟲系統依賴套件
echo ========================================
echo.

REM 取得當前目錄
set CURRENT_DIR=%~dp0

echo 正在安裝套件...
echo.

REM 使用 Portable Python 安裝套件
"%CURRENT_DIR%python\python.exe" -m pip install --upgrade pip
"%CURRENT_DIR%python\python.exe" -m pip install -r "%CURRENT_DIR%job_scraper_104\requirements_portable.txt"

echo.
echo ========================================
echo 正在安裝 Playwright 瀏覽器...
echo ========================================
echo.

"%CURRENT_DIR%python\python.exe" -m playwright install chromium

echo.
echo ========================================
echo 安裝完成！
echo ========================================
echo.
echo 接下來請執行：
echo 1. start_chrome_cdp.bat （啟動 Chrome）
echo 2. run_scraper.bat （執行爬蟲）
echo.
pause
