@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo 104 職缺爬蟲系統 - 自動安裝設置
echo ========================================
echo.

REM 取得當前目錄
set CURRENT_DIR=%~dp0

REM 檢查是否已有 Python 環境
if exist "%CURRENT_DIR%python\python.exe" (
    echo [檢查] 發現現有 Python 環境
    echo.
    choice /C YN /M "是否要重新安裝 Python 環境？(Y=是, N=否)"
    if errorlevel 2 goto :install_packages
    if errorlevel 1 goto :download_python
) else (
    echo [檢查] 未發現 Python 環境，開始自動安裝...
    echo.
)

:download_python
echo ========================================
echo 步驟 1/4: 下載 Python Embeddable
echo ========================================
echo.

REM 設定 Python 版本
set PYTHON_VERSION=3.11.8
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip
set PYTHON_ZIP=%TEMP%\python-embed.zip

echo 正在下載 Python %PYTHON_VERSION% Embeddable...
echo 下載位置: %PYTHON_URL%
echo.

REM 使用 PowerShell 下載
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_ZIP%'}"

if not exist "%PYTHON_ZIP%" (
    echo [錯誤] Python 下載失敗！
    echo.
    echo 請手動下載並解壓縮到 python\ 目錄：
    echo %PYTHON_URL%
    echo.
    pause
    exit /b 1
)

echo [成功] Python 下載完成
echo.

echo ========================================
echo 步驟 2/4: 解壓縮 Python
echo ========================================
echo.

REM 建立 python 目錄
if not exist "%CURRENT_DIR%python" mkdir "%CURRENT_DIR%python"

echo 正在解壓縮 Python...
powershell -Command "& {Expand-Archive -Path '%PYTHON_ZIP%' -DestinationPath '%CURRENT_DIR%python' -Force}"

if not exist "%CURRENT_DIR%python\python.exe" (
    echo [錯誤] Python 解壓縮失敗！
    pause
    exit /b 1
)

echo [成功] Python 解壓縮完成
echo.

REM 刪除下載的 zip 檔案
del "%PYTHON_ZIP%"

echo ========================================
echo 步驟 3/4: 配置 Python 環境
echo ========================================
echo.

REM 修改 python311._pth 以啟用 site-packages
echo 正在配置 Python 環境...

set PTH_FILE=%CURRENT_DIR%python\python311._pth

REM 備份原始檔案
if exist "%PTH_FILE%" (
    copy "%PTH_FILE%" "%PTH_FILE%.bak" >nul
)

REM 建立新的 _pth 檔案
(
echo python311.zip
echo .
echo.
echo # Uncomment to run site.main automatically
echo import site
) > "%PTH_FILE%"

echo [成功] Python 環境配置完成
echo.

echo ========================================
echo 步驟 4/4: 安裝 pip
echo ========================================
echo.

REM 下載 get-pip.py
set GET_PIP_URL=https://bootstrap.pypa.io/get-pip.py
set GET_PIP_FILE=%CURRENT_DIR%get-pip.py

echo 正在下載 get-pip.py...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%GET_PIP_URL%' -OutFile '%GET_PIP_FILE%'}"

if not exist "%GET_PIP_FILE%" (
    echo [錯誤] get-pip.py 下載失敗！
    pause
    exit /b 1
)

echo 正在安裝 pip...
"%CURRENT_DIR%python\python.exe" "%GET_PIP_FILE%"

if errorlevel 1 (
    echo [錯誤] pip 安裝失敗！
    pause
    exit /b 1
)

echo [成功] pip 安裝完成
echo.

REM 刪除 get-pip.py
del "%GET_PIP_FILE%"

:install_packages
echo ========================================
echo 步驟 5/6: 安裝 Python 套件
echo ========================================
echo.

echo 正在安裝必要套件...
echo.

REM 升級 pip
"%CURRENT_DIR%python\python.exe" -m pip install --upgrade pip

REM 安裝套件
"%CURRENT_DIR%python\python.exe" -m pip install -r "%CURRENT_DIR%job_scraper_104\requirements_portable.txt"

if errorlevel 1 (
    echo [錯誤] 套件安裝失敗！
    pause
    exit /b 1
)

echo [成功] 套件安裝完成
echo.

echo ========================================
echo 步驟 6/6: 安裝 Playwright 瀏覽器
echo ========================================
echo.

echo 正在安裝 Playwright Chromium 瀏覽器...
echo 這可能需要幾分鐘時間...
echo.

"%CURRENT_DIR%python\python.exe" -m playwright install chromium

if errorlevel 1 (
    echo [警告] Playwright 瀏覽器安裝失敗！
    echo 您可以稍後手動執行：
    echo python\python.exe -m playwright install chromium
    echo.
)

echo ========================================
echo 安裝完成！
echo ========================================
echo.

REM 顯示安裝資訊
echo Python 版本：
"%CURRENT_DIR%python\python.exe" --version
echo.

echo 已安裝的套件：
"%CURRENT_DIR%python\python.exe" -m pip list | findstr /C:"requests" /C:"schedule" /C:"PyYAML" /C:"playwright"
echo.

echo ========================================
echo 下一步操作：
echo ========================================
echo.
echo 1. 檢查並調整 start_chrome_cdp.bat 中的 Chrome 路徑
echo 2. 執行 start_chrome_cdp.bat 啟動 Chrome
echo 3. 執行 run_scraper.bat 開始爬取職缺
echo.
echo 詳細說明請參閱：
echo   - QUICK_START.md （快速開始）
echo   - README_PORTABLE.md （完整指南）
echo.

pause
