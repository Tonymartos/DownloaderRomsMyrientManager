# Modules - Refactored Code Structure

## 📁 Structure Overview

The `myrient_manager.py` has been refactored into modular components for better organization and maintainability.

```
modules/
├── __init__.py          # Module initialization
├── utils.py             # Utility functions and constants
├── fetcher.py           # HTTP requests and HTML parsing
├── analyzer.py          # Language/region detection and analysis
├── ui.py                # User interface functions
└── extractor.py         # ZIP file extraction functions
```

## 📦 Module Descriptions

### `utils.py` - Utility Functions
**Purpose:** Common utilities used across all modules

**Contains:**
- `Colors` class - ANSI color codes for terminal output
- `convert_bytes_to_readable()` - Convert bytes to human-readable format (KB, MB, GB, etc.)
- `validate_url()` - Validate Myrient URLs
- `ask_yes_no()` - Interactive yes/no prompt with default behavior

**Example:**
```python
from modules.utils import Colors, convert_bytes_to_readable

size = convert_bytes_to_readable(1024 * 1024 * 500)  # "500.0 MiB"
print(f"{Colors.GREEN}File size: {size}{Colors.END}")
```

---

### `fetcher.py` - Data Fetching
**Purpose:** Handle all HTTP requests and HTML parsing from Myrient

**Contains:**
- `fetch_directory_listing()` - Fetch and parse directory listing from Myrient URL
- `parse_size()` - Parse file size text to bytes

**Features:**
- URL decoding for special characters
- Demo file filtering
- Error handling for network issues
- Size parsing with multiple unit formats

**Example:**
```python
from modules.fetcher import fetch_directory_listing

files = fetch_directory_listing(url, include_demos=False)
# Returns: [{'name': '...', 'url': '...', 'size': bytes, 'size_text': '...'}]
```

---

### `analyzer.py` - Analysis Functions
**Purpose:** Analyze files for languages, regions, and detect patterns

**Contains:**
- `analyze_available_languages_and_regions()` - Detect all languages and regions in files
- `extract_key_words()` - Extract meaningful keywords from game titles
- `extract_disc_info()` - Extract disc numbers from filenames
- `detect_european_countries()` - Detect specific European countries for a language

**Features:**
- Multi-language pattern detection (11 languages)
- Continental region grouping (5 regions)
- Keyword-based duplicate detection
- Multi-disc game support

**Example:**
```python
from modules.analyzer import analyze_available_languages_and_regions

analysis = analyze_available_languages_and_regions(files)
# Returns: {
#     'languages': {'Es': 880, 'En': 3380, ...},
#     'regions': {'Europe': 3912, 'Americas': 1920, ...},
#     'language_examples': {...},
#     'region_examples': {...}
# }
```

---

### `ui.py` - User Interface
**Purpose:** Handle all user interaction and display formatting

**Contains:**
- `print_banner()` - Display welcome banner
- `show_available_options()` - Display detected languages and regions
- `ask_confirmation()` - Confirmation prompt before download
- `show_search_mode_menu()` - Display search mode options
- `show_step_separator()` - Visual step indicators

**Features:**
- Color-coded output
- Formatted tables and lists
- Progress indicators
- Step-by-step workflow display

**Example:**
```python
from modules.ui import print_banner, show_available_options

print_banner()
show_available_options(analysis)
```

---

### `extractor.py` - File Extraction
**Purpose:** Handle ZIP file extraction with progress tracking

**Contains:**
- `extract_downloaded_files()` - Extract all ZIP files in directory with progress

**Features:**
- Progress tracking (updates every 5 files)
- Error handling for corrupted ZIPs
- Automatic directory creation
- Extraction summary statistics

**Example:**
```python
from modules.extractor import extract_downloaded_files

extracted, errors = extract_downloaded_files('psx_downloads')
# Returns: (extracted_count, error_count)
```

---

## 🔄 Migration Plan

### Phase 1: ✅ **Completed**
- [x] Create module directory structure
- [x] Extract utility functions → `utils.py`
- [x] Extract fetcher functions → `fetcher.py`
- [x] Extract analyzer functions → `analyzer.py`
- [x] Extract UI functions → `ui.py`
- [x] Extract extractor functions → `extractor.py`

### Phase 2: 🚧 **In Progress**
- [ ] Create `filter.py` - File filtering and prioritization logic
- [ ] Create `downloader.py` - Download management functions
- [ ] Create `config.py` - Configuration and language presets
- [ ] Update `myrient_manager.py` to import from modules

### Phase 3: 📋 **Planned**
- [ ] Add unit tests for each module
- [ ] Update documentation
- [ ] Add type hints to all functions
- [ ] Create module integration tests

---

## 🎯 Benefits of Modular Structure

### ✅ **Better Organization**
- Clear separation of concerns
- Easy to locate specific functionality
- Logical grouping of related functions

### ✅ **Improved Maintainability**
- Changes isolated to specific modules
- Easier to debug and test
- Clear dependencies between components

### ✅ **Code Reusability**
- Modules can be imported independently
- Functions can be used in other projects
- Easier to create new tools using existing modules

### ✅ **Scalability**
- Easy to add new features
- Can extend modules without affecting others
- Clear structure for new contributors

---

## 📚 Usage in Main Program

Once complete, the main program will use imports like:

```python
from modules.utils import Colors, ask_yes_no, validate_url
from modules.fetcher import fetch_directory_listing
from modules.analyzer import analyze_available_languages_and_regions
from modules.ui import print_banner, show_available_options
from modules.extractor import extract_downloaded_files

def main():
    print_banner()
    
    # Fetch files
    files = fetch_directory_listing(url)
    
    # Analyze
    analysis = analyze_available_languages_and_regions(files)
    
    # Show options
    show_available_options(analysis)
    
    # Download logic...
    
    # Extract
    if ask_yes_no("Extract files?"):
        extract_downloaded_files(output_dir)
```

---

## 🔍 Next Steps

1. **Complete remaining modules:**
   - `filter.py` - Priority filtering and duplicate detection
   - `downloader.py` - Download management and progress tracking
   - `config.py` - Language configurations and presets

2. **Refactor main file:**
   - Update `myrient_manager.py` to use module imports
   - Remove duplicated code
   - Clean up and simplify main logic

3. **Testing:**
   - Create test suite for each module
   - Verify functionality remains unchanged
   - Test edge cases

4. **Documentation:**
   - Add docstrings to all functions
   - Create API documentation
   - Update user documentation

---

## 💡 Design Principles

- **Single Responsibility:** Each module has one clear purpose
- **Low Coupling:** Modules depend on minimal external code
- **High Cohesion:** Related functionality grouped together
- **DRY (Don't Repeat Yourself):** Shared code in utils module
- **Clear Interfaces:** Well-defined function signatures

---

Created: October 17, 2025
Last Updated: October 17, 2025
