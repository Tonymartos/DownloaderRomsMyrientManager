#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2025 Myrient ROM Manager Contributors
# This file is licensed under the GNU General Public License v3.0
# See LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt for details.
"""
Universal build script for creating executables
Works on Windows, Linux, and macOS
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

# Fix Windows console encoding for emojis
if platform.system() == "Windows":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def get_system_name():
    """Get normalized system name"""
    system = platform.system().lower()
    # macOS reports as 'darwin', normalize to 'macos'
    if system == "darwin":
        return "macos"
    return system

def run_command(cmd, shell=False):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=shell, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def install_pyinstaller():
    """Install PyInstaller if not present"""
    print("📦 Installing PyInstaller...")
    return run_command([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_directories():
    """Create necessary directories"""
    Path("dist").mkdir(exist_ok=True)
    Path("build").mkdir(exist_ok=True)
    
    system = get_system_name()
    dist_dir = Path("dist") / system
    dist_dir.mkdir(exist_ok=True, parents=True)
    return dist_dir

def build_executable(script_name, exe_name, dist_dir):
    """Build a single executable"""
    print(f"📦 Building {exe_name}...")
    
    system = get_system_name()
    
    # Use the same Python executable that's running this script
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        f"--name={exe_name}",
        "--console",
        "--noupx",  # Disable UPX compression (can cause issues)
        script_name
    ]
    
    # Add hidden imports for all dependencies
    pyinstaller_cmd.extend([
        "--hidden-import=modules",
        "--hidden-import=modules.analyzer",
        "--hidden-import=modules.extractor",
        "--hidden-import=modules.fetcher",
        "--hidden-import=modules.ui",
        "--hidden-import=modules.utils",
        "--hidden-import=requests",
        "--hidden-import=bs4",
        "--hidden-import=urllib3",
        "--collect-all=requests",
        "--collect-all=bs4",
        "--copy-metadata=requests",
    ])
    
    # Add icon if exists
    if Path("icon.ico").exists():
        pyinstaller_cmd.extend(["--icon=icon.ico"])
    
    # Add data files
    if system == "windows":
        pyinstaller_cmd.extend(["--add-data=README.md;."])
    else:
        pyinstaller_cmd.extend(["--add-data=README.md:."])
    
    success = run_command(pyinstaller_cmd)
    
    if success:
        # Move executable to system-specific folder
        if system == "windows":
            exe_file = Path("dist") / f"{exe_name}.exe"
            target = dist_dir / f"{exe_name}.exe"
        else:
            exe_file = Path("dist") / exe_name
            target = dist_dir / exe_name
        
        if exe_file.exists():
            shutil.copy2(exe_file, target)
            print(f"✅ {exe_name} created successfully")
            return True
    
    print(f"❌ Failed to build {exe_name}")
    return False

def create_readme(dist_dir):
    """Create README file for the distribution"""
    system = get_system_name()
    
    if system == "windows":
        exe_suffix = ".exe"
    else:
        exe_suffix = ""
    
    readme_content = f"""🎮 Myrient ROM Manager - {system.title()} Executable

USAGE:
======

Interactive Mode (All-in-one tool):
   ./myrient-manager{exe_suffix}

This executable provides:
  • Interactive menu to browse and download ROMs
  • Preview mode to see available files
  • Batch download capabilities
  • Command-line options for automation

IMPORTANT - DOWNLOAD LOCATION:
==============================
⚠️  Downloaded ROMs will be saved in the SAME DIRECTORY as the executable!

By default, a "downloads" folder will be created next to the executable:
  • Windows: Same folder as myrient-manager.exe
  • macOS/Linux: Same folder as myrient-manager

Example directory structure after download:
  my-roms-folder/
    ├── myrient-manager{exe_suffix}    ← Executable
    └── downloads/                     ← ROMs downloaded here
        ├── Game1.zip
        ├── Game2.zip
        └── ...

TIP: Place the executable in the folder where you want your ROMs!

NOTES:
======
- Internet connection required
- Respect Myrient's terms of service
- For support: https://github.com/Tonymartos/DownloaderRomsMyrientManager

SYSTEM: {platform.system()} {platform.release()}
ARCHITECTURE: {platform.machine()}
PYTHON VERSION: {platform.python_version()}
"""

    readme_path = dist_dir / "README.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"📄 README created at {readme_path}")

def main():
    """Main build function"""
    print("🔨 Myrient ROM Manager - Universal Build Script")
    print(f"🖥️  System: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {platform.python_version()}")
    print(f"🏗️  Architecture: {platform.machine()}")
    print()
    
    # Install PyInstaller
    if not install_pyinstaller():
        print("❌ Failed to install PyInstaller")
        return False
    
    # Create directories
    dist_dir = create_directories()
    print(f"📁 Distribution directory: {dist_dir}")
    
    # Build only myrient-manager executable
    builds = [
        ("myrient_manager.py", "myrient-manager")
    ]
    
    success_count = 0
    for script, name in builds:
        if Path(script).exists():
            if build_executable(script, name, dist_dir):
                success_count += 1
        else:
            print(f"⚠️  Warning: {script} not found, skipping...")
    
    # Create README
    create_readme(dist_dir)
    
    # Summary
    print("\n" + "="*50)
    print(f"🎉 Build completed! {success_count}/1 executable built")
    print(f"📁 Executable available in: {dist_dir}")
    
    if success_count > 0:
        print("\n📋 Built executable:")
        for file in dist_dir.glob("myrient-*"):
            print(f"   - {file.name}")
    
    print("\n💡 Usage tip:")
    system = get_system_name()
    if system == "windows":
        print("   Double-click myrient-manager.exe or run from Command Prompt")
    else:
        print("   Make executable: chmod +x myrient-manager")
        print("   Run: ./myrient-manager")
    
    return success_count > 0

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)