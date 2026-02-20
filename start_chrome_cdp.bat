@echo off
chcp 65001 >nul
echo ========================================
echo 啟動 Chrome 瀏覽器（CDP 模式）
echo ========================================
echo.

REM 取得當前目錄
set CURRENT_DIR=%~dp0

REM 建立 Chrome 用戶資料目錄
if not exist "%CURRENT_DIR%chrome_user_data" (
    mkdir "%CURRENT_DIR%chrome_user_data"
)

echo 正在啟動 Chrome...
echo 端口: 9527
echo 用戶資料目錄: %CURRENT_DIR%chrome_user_data
echo.

REM 啟動 Chrome（請根據實際 Chrome 安裝路徑調整）
REM 常見路徑：
REM   C:\Program Files\Google\Chrome\Application\chrome.exe
REM   C:\Program Files (x86)\Google\Chrome\Application\chrome.exe

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9527 --user-data-dir="%CURRENT_DIR%chrome_user_data"

echo.
echo Chrome 已啟動！
echo 請保持此視窗開啟
echo.
echo 如果 Chrome 沒有啟動，請檢查 Chrome 安裝路徑
echo 並修改此批次檔中的路徑
echo.
pause
