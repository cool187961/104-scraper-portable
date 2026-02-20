@echo off
chcp 65001 >nul
echo ========================================
echo 104 職缺爬蟲系統 - 排程模式
echo ========================================
echo.

REM 取得當前目錄
set CURRENT_DIR=%~dp0

echo 配置資訊：
echo   排程時間: 每天 08:00
echo   關鍵字: 資料工程、資料分析、RPA自動化
echo   每個關鍵字抓取數量: 50 筆
echo.
echo 提示：請確保 Chrome 已使用 CDP 模式啟動
echo       如果尚未啟動，請先執行 start_chrome_cdp.bat
echo.
echo 按 Ctrl+C 停止排程
echo.
pause

echo.
echo 正在啟動排程...
echo.

REM 切換到程式目錄
cd /d "%CURRENT_DIR%"

REM 執行爬蟲（排程模式）
"%CURRENT_DIR%python\python.exe" job_scraper_104\main.py --mode schedule

pause
