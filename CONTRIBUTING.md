# 🤝 Contributing to Myrient ROM Manager

Thank you for your interest in contributing to this project! This guide will help you get started with contributing or creating forks for other platforms.

## 🍴 Creating Forks for Other Platforms

### Why Fork?

This project is specifically designed for **Myrient platform**. If you want to support other ROM download sites, forking is the recommended approach because:

- Each platform has different HTML structures
- URL patterns and navigation differ
- File naming conventions vary
- Different region/language systems may be needed

### 🏗️ Architecture Overview

The project is structured in a modular way to facilitate forking:

```
downloadRomsMyrientManager/
├── downloadroms.py          # Core download logic
├── myrient_manager.py       # Interactive UI framework  
├── preview_downloadroms.py  # Preview functionality
└── test_downloadroms.py     # Test suite
```

### 🔧 Components You Can Reuse

**✅ Highly Reusable:**
- **Interactive menu system** (`myrient_manager.py` lines 50-110)
- **Color output classes** (`Colors` class)
- **Download progress tracking**
- **File size formatting** (`convert_bytes_to_readable`)
- **Command-line argument parsing**
- **Error handling patterns**

**🔄 Platform-Specific (Need Modification):**
- **HTML parsing logic** (`fetch_directory_listing`)
- **URL validation** (`validate_url`)
- **File pattern matching** (`extract_region`, `extract_base_title`)
- **Region priority systems** (`REGION_PRIORITY`)

### 📝 Fork Checklist

When creating a fork for another platform:

1. **Setup**
   - [ ] Fork the repository
   - [ ] Update project name and description
   - [ ] Modify `pyproject.toml` with new package name

2. **Core Modifications**
   - [ ] Update `fetch_directory_listing()` for target platform's HTML
   - [ ] Modify region detection patterns
   - [ ] Adapt file filtering logic
   - [ ] Update URL validation rules

3. **Configuration**
   - [ ] Update `REGION_PRIORITY` for your target audience
   - [ ] Modify language configuration in interactive mode
   - [ ] Adapt file naming patterns

4. **Documentation**
   - [ ] Update README with platform-specific information
   - [ ] Add examples for your target platform
   - [ ] Document any new configuration options
   - [ ] Credit original project

5. **Testing**
   - [ ] Test with actual URLs from target platform
   - [ ] Verify region filtering works correctly
   - [ ] Test both interactive and CLI modes

### 🎯 Popular Platform Adaptation Ideas

**Archive.org Internet Arcade:**
- Different HTML structure (archive.org specific)
- Focus on arcade ROM collections
- Different file organization

**RetroArch ROM sites:**
- Multiple format support (not just .zip)
- Different region naming conventions
- Core-specific organization

**Console-specific sites:**
- Platform-focused filtering
- Generation-based organization
- System-specific file types

### 🤝 Community Guidelines

**When creating forks:**
1. **Credit the original** - Link back to this repository
2. **Follow similar naming** - `platform-rom-manager` format suggested
3. **Maintain ethical standards** - Respect platform terms of service
4. **Share improvements** - Consider contributing generic improvements back

**Contribution types welcome:**
- 🐛 Bug fixes
- ✨ New features for core architecture
- 📚 Documentation improvements
- 🧪 Additional test cases
- 🌍 Translation improvements

### 📞 Getting Help

**For fork-specific questions:**
- Open an issue with `[FORK]` prefix
- Describe your target platform
- Share specific technical challenges

**For contributing to core:**
- Follow standard GitHub pull request process
- Include tests for new features
- Update documentation as needed

## 📋 Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/your-platform-rom-manager
cd your-platform-rom-manager

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
python -m pytest test_downloadroms.py
```

## 🔍 Code Style

- Follow PEP 8 for Python code style
- Use descriptive variable names
- Add docstrings for new functions
- Include type hints where helpful
- Maintain existing error handling patterns

## 📊 Example Fork: Archive.org Adapter

Here's a simplified example of what adapting for Archive.org might look like:

```python
# Modified fetch_directory_listing for Archive.org
def fetch_directory_listing(url, include_demos=False):
    # Archive.org has different HTML structure
    # Would need to parse their specific format
    # Example: looking for different CSS classes/patterns
    pass

# Modified region detection for Archive.org naming
def extract_region(filename):
    # Archive.org might use different region patterns
    # Adapt the regex patterns accordingly
    pass
```

## 🎯 Success Stories

We'd love to feature successful forks! If you create a working fork for another platform:

1. Let us know by opening an issue
2. We'll add it to a "Community Forks" section
3. Cross-promote to help users find the right tool

---

**Remember**: The goal is to help preserve gaming history across all platforms while respecting content creators and platform policies. Happy forking! 🎮