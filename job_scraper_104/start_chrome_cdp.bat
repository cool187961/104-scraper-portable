@echo off
echo ========================================
echo 啟動 Chrome 瀏覽器（CDP 模式）
echo ========================================
echo.
echo 正在啟動 Chrome...
echo 端口: 9527
echo 用戶資料目錄: E:\Chrome User Data
echo.

start chrome.exe --remote-debugging-port=9527 --user-data-dir="E:\Chrome User Data"

echo.
echo Chrome 已啟動！
echo 請保持此視窗開啟
echo.
echo 按任意鍵關閉此視窗...
pause > nul
