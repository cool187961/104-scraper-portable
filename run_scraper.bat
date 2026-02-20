@echo off
chcp 65001 >nul
echo ========================================
echo 104 職缺爬蟲系統 - 手動模式
echo ========================================
echo.

REM 取得當前目錄
set CURRENT_DIR=%~dp0

echo.
echo 正在執行爬蟲...
echo.

REM 切換到程式目錄
cd /d "%CURRENT_DIR%"

REM 執行爬蟲（手動模式）
"%CURRENT_DIR%python\python.exe" job_scraper_104\main.py --mode manual

echo.
echo ========================================
echo 執行完成！
echo ========================================
echo.
echo 請查看輸出目錄: %CURRENT_DIR%data\jobs
echo 日誌檔案: %CURRENT_DIR%logs\scraper.log
echo.
pause
