# 建立 Portable Python 環境說明

由於 Python 環境較大（約 100-200MB），建議使用以下方式之一：

## 方案一：使用 Python Embeddable（推薦）

1. 下載 Python 3.11 Embeddable 版本：
   https://www.python.org/ftp/python/3.11.8/python-3.11.8-embed-amd64.zip

2. 解壓縮到 `104_Scraper_Portable\python\` 目錄

3. 修改 `python311._pth` 檔案，取消註解：
   ```
   import site
   ```

4. 下載 get-pip.py：
   https://bootstrap.pypa.io/get-pip.py

5. 安裝 pip：
   ```bash
   python\python.exe get-pip.py
   ```

6. 執行 `install_dependencies.bat` 安裝套件

## 方案二：複製現有環境

從 `D:\miniconda3\envs\auto_env\` 複製以下檔案/資料夾到 `104_Scraper_Portable\python\`：

```
python.exe
python311.dll
python3.dll
pythonw.exe
Lib\
Scripts\
DLLs\
```

## 方案三：使用虛擬環境

在 `104_Scraper_Portable\` 目錄執行：

```bash
D:\miniconda3\envs\auto_env\python.exe -m venv python
python\Scripts\activate
pip install -r job_scraper_104\requirements_portable.txt
```

---

**注意**：由於檔案大小限制，Python 環境未包含在此資料夾中，請依照上述方式之一建立。
