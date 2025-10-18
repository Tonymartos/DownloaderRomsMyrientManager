#!/bin/bash
# Build script for creating executables on Linux/macOS

echo "🔨 Building Myrient ROM Manager executables..."

# Install PyInstaller if not present
pip install pyinstaller

# Create dist directory
mkdir -p dist
mkdir -p build

echo "📦 Building Interactive Mode (myrient_manager)..."
pyinstaller --onefile \
    --name="myrient-manager" \
    --add-data="README.md:." \
    --console \
    --icon=icon.ico \
    myrient_manager.py

echo "📦 Building CLI Mode (downloadroms)..."
pyinstaller --onefile \
    --name="myrient-download" \
    --add-data="README.md:." \
    --console \
    --icon=icon.ico \
    downloadroms.py

echo "📦 Building Preview Mode (preview_downloadroms)..."
pyinstaller --onefile \
    --name="myrient-preview" \
    --add-data="README.md:." \
    --console \
    --icon=icon.ico \
    preview_downloadroms.py

# Move executables to a clean distribution folder
mkdir -p dist/linux
cp dist/myrient-manager dist/linux/
cp dist/myrient-download dist/linux/
cp dist/myrient-preview dist/linux/

echo "✅ Linux executables created in dist/linux/"
echo "📁 Available executables:"
echo "   - myrient-manager    (Interactive mode)"
echo "   - myrient-download   (CLI mode)"
echo "   - myrient-preview    (Preview mode)"

# Create usage instructions
cat > dist/linux/README.txt << 'EOF'
🎮 Myrient ROM Manager - Linux Executables

USAGE:
======

1. Interactive Mode (Recommended for beginners):
   ./myrient-manager

2. Command Line Mode:
   ./myrient-download "https://myrient.erista.me/files/..." output_folder
   ./myrient-download "URL" folder --demos --quiet

3. Preview Mode (see what would be downloaded):
   ./myrient-preview "https://myrient.erista.me/files/..."

NOTES:
======
- Make sure executables have execute permissions: chmod +x myrient-*
- Internet connection required
- Respect Myrient's terms of service
- For support: https://github.com/Tonymartos/DownloaderRomsMyrientManager

EOF

echo ""
echo "🎉 Build completed! Check dist/linux/ folder"