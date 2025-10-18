@echo off
REM Build script for creating executables on Windows

echo 🔨 Building Myrient ROM Manager executables...

REM Install PyInstaller if not present
pip install pyinstaller

REM Create dist directory
if not exist "dist" mkdir dist
if not exist "build" mkdir build

echo 📦 Building Interactive Mode (myrient_manager)...
pyinstaller --onefile ^
    --name="myrient-manager" ^
    --add-data="README.md;." ^
    --console ^
    --icon=icon.ico ^
    myrient_manager.py

echo 📦 Building CLI Mode (downloadroms)...
pyinstaller --onefile ^
    --name="myrient-download" ^
    --add-data="README.md;." ^
    --console ^
    --icon=icon.ico ^
    downloadroms.py

echo 📦 Building Preview Mode (preview_downloadroms)...
pyinstaller --onefile ^
    --name="myrient-preview" ^
    --add-data="README.md;." ^
    --console ^
    --icon=icon.ico ^
    preview_downloadroms.py

REM Move executables to a clean distribution folder
if not exist "dist\windows" mkdir dist\windows
copy dist\myrient-manager.exe dist\windows\
copy dist\myrient-download.exe dist\windows\
copy dist\myrient-preview.exe dist\windows\

echo ✅ Windows executables created in dist\windows\
echo 📁 Available executables:
echo    - myrient-manager.exe    (Interactive mode)
echo    - myrient-download.exe   (CLI mode)
echo    - myrient-preview.exe    (Preview mode)

REM Create usage instructions
echo 🎮 Myrient ROM Manager - Windows Executables > dist\windows\README.txt
echo. >> dist\windows\README.txt
echo USAGE: >> dist\windows\README.txt
echo ====== >> dist\windows\README.txt
echo. >> dist\windows\README.txt
echo 1. Interactive Mode (Recommended for beginners): >> dist\windows\README.txt
echo    myrient-manager.exe >> dist\windows\README.txt
echo. >> dist\windows\README.txt
echo 2. Command Line Mode: >> dist\windows\README.txt
echo    myrient-download.exe "https://myrient.erista.me/files/..." output_folder >> dist\windows\README.txt
echo    myrient-download.exe "URL" folder --demos --quiet >> dist\windows\README.txt
echo. >> dist\windows\README.txt
echo 3. Preview Mode (see what would be downloaded): >> dist\windows\README.txt
echo    myrient-preview.exe "https://myrient.erista.me/files/..." >> dist\windows\README.txt
echo. >> dist\windows\README.txt
echo NOTES: >> dist\windows\README.txt
echo ====== >> dist\windows\README.txt
echo - Internet connection required >> dist\windows\README.txt
echo - Respect Myrient's terms of service >> dist\windows\README.txt
echo - For support: https://github.com/Tonymartos/DownloaderRomsMyrientManager >> dist\windows\README.txt

echo.
echo 🎉 Build completed! Check dist\windows\ folder
pause