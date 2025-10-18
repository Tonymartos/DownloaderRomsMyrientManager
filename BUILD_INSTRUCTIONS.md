# 🔨 Build Instructions for All Platforms

This document explains how to build executables for Windows, macOS, and Linux.

## 📋 Prerequisites

- Python 3.7 or higher
- PyInstaller (`pip install pyinstaller`)
- Git (for version control)

## 🐧 Linux Build

**System Requirements:**
- Any Linux distribution (Ubuntu, Fedora, Arch, etc.)
- Python 3.7+

**Steps:**

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 2. Run build script
python build.py

# 3. Executables will be in dist/linux/
ls -lh dist/linux/
```

**Output Files:**
- `myrient-manager` - Interactive mode
- `myrient-download` - Command-line mode
- `myrient-preview` - Preview mode

## 🪟 Windows Build

**System Requirements:**
- Windows 10/11
- Python 3.7+ (from python.org)
- Command Prompt or PowerShell

**Steps:**

```cmd
# 1. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 2. Run build script
python build.py

# 3. Executables will be in dist\windows\
dir dist\windows\
```

**Alternative - Using build_windows.bat:**

```cmd
# Simply double-click or run:
build_windows.bat
```

**Output Files:**
- `myrient-manager.exe` - Interactive mode
- `myrient-download.exe` - Command-line mode
- `myrient-preview.exe` - Preview mode

## 🍎 macOS Build

**System Requirements:**
- macOS 10.13 (High Sierra) or newer
- Python 3.7+ (use Homebrew: `brew install python`)
- Terminal

**Steps:**

```bash
# 1. Install Python (if not already installed)
brew install python

# 2. Install dependencies
pip3 install -r requirements.txt
pip3 install pyinstaller

# 3. Run build script
python3 build.py

# 4. Executables will be in dist/macos/
ls -lh dist/macos/
```

**Alternative - Using build script:**

```bash
# Make executable and run:
chmod +x build_linux.sh
./build_linux.sh
```

**Output Files:**
- `myrient-manager` - Interactive mode
- `myrient-download` - Command-line mode
- `myrient-preview` - Preview mode

**Important for macOS:**
After downloading, you may need to remove the quarantine attribute:

```bash
xattr -d com.apple.quarantine myrient-manager
xattr -d com.apple.quarantine myrient-download
xattr -d com.apple.quarantine myrient-preview
```

## 🎯 Universal Build Script

The `build.py` script automatically detects your OS and creates executables in the appropriate `dist/` subfolder:

- **Linux** → `dist/linux/`
- **Windows** → `dist/windows/`
- **macOS** → `dist/macos/`

## 📦 Creating a Release

After building on each platform:

1. **Test the executables** on their target platform
2. **Compress the dist folders:**

```bash
# Linux/macOS
cd dist
tar -czf myrient-manager-linux-x64.tar.gz linux/
tar -czf myrient-manager-macos-x64.tar.gz macos/
zip -r myrient-manager-windows-x64.zip windows/

# Windows (PowerShell)
Compress-Archive -Path dist\windows -DestinationPath myrient-manager-windows-x64.zip
```

3. **Upload to GitHub Releases:**
   - Go to: https://github.com/Tonymartos/DownloaderRomsMyrientManager/releases
   - Click "Draft a new release"
   - Upload the compressed files
   - Add release notes

## 🔧 Troubleshooting

### PyInstaller not found

```bash
pip install --upgrade pyinstaller
```

### Permission denied (Linux/macOS)

```bash
chmod +x build.py
chmod +x build_linux.sh
```

### "Cannot find Python" (Windows)

Make sure Python is added to PATH during installation.

### macOS "App is damaged" error

Remove quarantine attribute:

```bash
xattr -d com.apple.quarantine myrient-manager
```

## 📊 Build Output

Each platform build creates:

```
dist/
├── linux/
│   ├── myrient-manager
│   ├── myrient-download
│   ├── myrient-preview
│   └── README.txt
├── windows/
│   ├── myrient-manager.exe
│   ├── myrient-download.exe
│   ├── myrient-preview.exe
│   └── README.txt
└── macos/
    ├── myrient-manager
    ├── myrient-download
    ├── myrient-preview
    └── README.txt
```

## 🚀 Automated Builds (Future)

Consider using GitHub Actions for automated cross-platform builds:

- Ubuntu runners for Linux builds
- Windows runners for Windows builds
- macOS runners for macOS builds

This would allow building all platforms from a single commit!

## 📝 Notes

- **Cross-compilation is NOT supported** by PyInstaller
- Each platform must be built on its native OS
- Virtual machines or CI/CD services can help build for multiple platforms
- Binary size varies by platform (typically 7-15 MB per executable)

## 🔗 Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [GitHub Releases Guide](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Python Packaging Guide](https://packaging.python.org/)
