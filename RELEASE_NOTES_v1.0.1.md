# Release Notes - Version 1.0.1# Release v1.0.1 - Improved Region & Language Detection



**Release Date:** October 18, 2025## 🎯 New Features



## 🎉 What's New- **Changed 'Americas' to 'USA'** for more direct and clearer region naming

- **Pre-analysis of languages per region** - System now analyzes files once at startup and reuses data for instant region selection

### ✨ Features- **Improved language detection** from region-specific files (USA, Europe, Asia, etc.)



#### 🖥️ Clear Screen for Better UX## 🐛 Bug Fixes

- Added automatic screen clearing at 7 strategic points in the workflow

- Each major section now displays in a clean, focused screen- **Fixed language code detection** - No longer captures words from game titles (e.g., "El" from "El Dorado")

- Improved visual clarity and reduced information overload- **Fixed regex pattern** - Now only extracts language codes from parentheses content

- Better user experience with professional-looking interface- **Fixed USA region** - Now properly detects language codes in USA/Americas files



#### 🚫 Smart ROM Filtering## ⚡ Performance Improvements

- **Automatically excludes revision and beta versions**

  - Filters out `(Rev)`, `(Rev 1)`, `(Rev 2)`, etc.- **Single analysis at startup** - Analyzes all files once instead of re-analyzing for each region selection

  - Filters out `(Beta)` versions- **Instant language options display** - Shows available languages immediately when selecting a region

  - Ensures you only download final/stable ROM releases- **Reduced processing time** - No redundant file scanning

  - Reduces clutter and saves bandwidth

## 📊 Technical Changes

#### 💾 Intelligent ZIP Management

- **Delete ZIPs immediately after extraction** (new!)- **Region mapping improvements:**

  - Asks once at the beginning if you want to delete ZIPs  - USA region now maps to: `(USA)`, `(U)`, `(Brazil)`, `(America)` files

  - Deletes each ZIP file right after successful extraction  - Europe region maps to: `(Europe)`, `(Spain)`, `(France)`, `(Germany)`, etc.

  - **Never uses double disk space** during extraction  - Asia region maps to: `(Japan)`, `(China)`, `(Korea)`, `(Asia)` files

  - Shows space freed in real-time for each file  

  - Only deletes successfully extracted files (keeps failed ones)- **Language extraction refinement:**

  - Summary shows total space freed at the end  - Only extracts codes from parentheses content

  - Validates against known language dictionary

#### 🧪 Improved Test Mode  - Splits multi-language entries correctly (e.g., "En,Es,Fr")

- Test mode now limited to **10 files** (was 20)

- Faster testing and validation- **New data structure:**

- Only available in development mode (not in compiled version)  - Added `languages_by_region` pre-computed dictionary

  - Added `language_full_names` for consistent naming

### 🐛 Bug Fixes  - Improved analysis return structure



#### 📜 License Correction (Important!)## 🔗 Links

- **Fixed LICENSE file**: Removed incorrect MIT license text

- Now contains only **GNU General Public License v3.0** (complete official text)- [Full Changelog](https://github.com/Tonymartos/DownloaderRomsMyrientManager/compare/v1.0.0...v1.0.1)

- Added proper copyright header for the project- [Download ROMs from Myrient](https://myrient.erista.me/)

- Updated `pyproject.toml` to specify `GPL-3.0-or-later`

- All Python files already had correct GPL v3 headers## 📦 Installation



#### 🧹 Code Cleanup```bash

- Removed all test files from repository:git clone https://github.com/Tonymartos/DownloaderRomsMyrientManager.git

  - `run_test.py`cd DownloaderRomsMyrientManager

  - `test_download.sh`pip install -r requirements.txt

  - `TEST_INSTRUCTIONS.md`python myrient_manager.py

- Cleaner repository structure```



## 📊 Technical Changes## 📝 Usage Example



### Modified Functions```bash

# Run the manager

#### `extract_downloaded_files(output_dir, delete_zips_after=False)`python myrient_manager.py

- **New parameter**: `delete_zips_after` - controls ZIP deletion behavior

- **Changed return**: Now returns `(extracted_count, error_count, deleted_count)`# Enter URL: https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/

  - Previously returned: `(extracted_count, error_count, successfully_extracted_zips)`# Select: 1 (Analyze entire collection)

- Deletes ZIPs immediately after extraction (if enabled)# System analyzes once and shows:

- Tracks and reports freed disk space#   - Available languages

#   - Available regions with file counts

#### `analyze_files_with_priorities(files, config, include_demos)`#   - Pre-analyzed languages per region

- Added regex filter: `r'\(Rev\s*\d*\)|\(Beta\)'`

- Automatically excludes revision and beta ROM versions# Select USA region -> Instantly shows available languages (En, Es, Pt, Fr, etc.)

- Adds excluded files to invalid list with reason```



#### Screen Clearing Points---

Added `os.system('clear')` at these locations:

1. **Line 52** - Initial banner (`print_banner`)**Full Diff:** [v1.0.0...v1.0.1](https://github.com/Tonymartos/DownloaderRomsMyrientManager/compare/v1.0.0...v1.0.1)

2. **Line 149** - Start of extraction (`extract_downloaded_files`)
3. **Line 758** - Exclusive games selection (`show_exclusive_games_options`)
4. **Line 875** - Analysis summary display
5. **Line 946** - Filter criteria selection
6. **Line 1473** - Download preview (`show_preview_with_priorities`)
7. **Line 1528** - Download start (`download_selected_files`)

## 📦 Installation

### From Source
```bash
git clone https://github.com/Tonymartos/DownloaderRomsMyrientManager.git
cd DownloaderRomsMyrientManager
pip install -r requirements.txt
python myrient_manager.py
```

### From Release
Download the compiled executable for your platform from the [Releases](https://github.com/Tonymartos/DownloaderRomsMyrientManager/releases) page.

## 🔄 Upgrade Notes

If upgrading from v1.0.0:
- No breaking changes
- All existing features remain compatible
- New ZIP deletion is opt-in (asks user)
- Rev/Beta filtering is automatic (no configuration needed)

## 📝 Example Usage

### New ZIP Deletion Workflow
```
📦 Do you want to extract the downloaded ZIP files? yes
🗑️  Delete ZIP files immediately after extraction to save disk space? yes

📦 Extracting: Game Title (Spain).zip
  ✅ Successfully extracted to: Game Title (Spain)/
  🗑️  Deleted ZIP file (freed 420.5 MiB)

📦 EXTRACTION SUMMARY:
✅ Extracted: 10
❌ Errors: 0
🗑️  Deleted ZIPs: 10
💾 Space freed: 3.7 GiB
```

### Rev/Beta Filtering
Files automatically excluded:
- ❌ `Game Title (Rev 1).zip` - Revision version
- ❌ `Game Title (Beta).zip` - Beta version
- ✅ `Game Title (Spain).zip` - Final version (included)

## 🙏 Acknowledgments

Thanks to all contributors and users who provided feedback!

## 📄 License

This project is licensed under the **GNU General Public License v3.0 or later**.
See [LICENSE](LICENSE) file for full text.

---

**Full Changelog**: [v1.0.0...v1.0.1](https://github.com/Tonymartos/DownloaderRomsMyrientManager/compare/v1.0.0...v1.0.1)
