# 🔄 GitHub Actions Workflows

This directory contains automated workflows for building and releasing the Myrient ROM Manager.

## 📋 Available Workflows

### 1. `build-releases.yml` - Release Builder

**Triggers:**
- When you push a version tag (e.g., `v1.0.0`, `v2.1.3`)
- Manually via GitHub Actions tab

**What it does:**
1. Builds executables for all 3 platforms in parallel:
   - 🐧 Linux (x64)
   - 🪟 Windows (x64)
   - 🍎 macOS (Universal - Intel + Apple Silicon)

2. Creates compressed archives:
   - `myrient-manager-linux-x64.tar.gz`
   - `myrient-manager-windows-x64.zip`
   - `myrient-manager-macos-universal.tar.gz`

3. Automatically creates a GitHub Release with:
   - All 3 platform archives
   - Release notes
   - Download instructions
   - Legal disclaimer

**How to use:**

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically:
# - Build for all platforms
# - Create a release
# - Upload the files
```

Or use the GitHub interface:
1. Go to "Actions" tab
2. Select "Build Multi-Platform Releases"
3. Click "Run workflow"
4. Enter a tag name (e.g., `v1.0.0`)

### 2. `test-build.yml` - Test Builder

**Triggers:**
- Every push to `main` or `develop` branches
- Every pull request to `main`

**What it does:**
1. Builds executables for all 3 platforms (without creating release)
2. Runs basic tests to verify executables exist
3. Uploads build artifacts (available for 3 days)
4. Provides build summary

**Purpose:**
- Catch build errors before releasing
- Test changes across all platforms
- Download test builds from Actions tab

**How to access test builds:**
1. Go to "Actions" tab
2. Click on a completed workflow run
3. Scroll to "Artifacts" section
4. Download the platform you want to test

## 🚀 Creating a Release

### Method 1: Using Git Tags (Recommended)

```bash
# 1. Make sure all changes are committed
git add .
git commit -m "Prepare release v1.0.0"
git push origin main

# 2. Create and push the tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 3. Wait for GitHub Actions to complete
# Check the "Actions" tab for progress
# Release will appear in "Releases" tab when done
```

### Method 2: Manual Trigger

1. Go to repository → **Actions** tab
2. Select **"Build Multi-Platform Releases"**
3. Click **"Run workflow"** button
4. Select branch: `main`
5. Click **"Run workflow"**

### Method 3: GitHub Releases UI

1. Go to repository → **Releases** tab
2. Click **"Draft a new release"**
3. Click **"Choose a tag"**
4. Type new tag (e.g., `v1.0.0`) and click **"Create new tag"**
5. Fill in release details
6. Click **"Publish release"**
7. GitHub Actions will automatically build and upload files

## 📦 What Gets Built

Each workflow run produces 3 platform-specific archives:

### Linux Archive (`myrient-manager-linux-x64.tar.gz`)
```
linux/
├── myrient-manager      (9.8 MB)
├── myrient-download     (7.4 MB)
├── myrient-preview      (9.8 MB)
└── README.txt
```

### Windows Archive (`myrient-manager-windows-x64.zip`)
```
windows/
├── myrient-manager.exe  (~10 MB)
├── myrient-download.exe (~8 MB)
├── myrient-preview.exe  (~10 MB)
└── README.txt
```

### macOS Archive (`myrient-manager-macos-universal.tar.gz`)
```
macos/
├── myrient-manager      (~10 MB)
├── myrient-download     (~8 MB)
├── myrient-preview      (~10 MB)
└── README.txt
```

## ⏱️ Build Times

Typical build times per platform:
- **Linux**: 2-3 minutes
- **Windows**: 3-4 minutes
- **macOS**: 3-4 minutes
- **Total**: ~10 minutes for all platforms

## 🔍 Monitoring Builds

### View Build Progress

1. Go to **Actions** tab
2. Click on the running workflow
3. Click on individual jobs to see logs

### Build Status Badges

Add to README.md:

```markdown
![Build Status](https://github.com/Tonymartos/DownloaderRomsMyrientManager/actions/workflows/build-releases.yml/badge.svg)
```

## 🐛 Troubleshooting

### Build Fails on One Platform

Check the logs for that specific platform:
1. Go to Actions → Failed workflow
2. Click on the failed job (e.g., "Build for Windows")
3. Expand the failed step
4. Read error messages

Common issues:
- **Dependency not found**: Update `requirements.txt`
- **PyInstaller fails**: Check `build.py` script
- **File not found**: Ensure all files are committed

### Release Not Created

Check:
- ✅ Tag pushed correctly: `git tag -l`
- ✅ Workflow completed successfully
- ✅ `GITHUB_TOKEN` has permissions (should be automatic)

### Artifacts Not Uploaded

Verify:
- ✅ All build jobs completed successfully
- ✅ Executables exist in `dist/` directory
- ✅ Archive creation step succeeded

## 🔐 Security

### Secrets Required

None! The workflow uses automatic `GITHUB_TOKEN` which is provided by GitHub.

### Permissions

The workflow needs:
- ✅ `contents: write` - To create releases (automatic)
- ✅ `actions: read` - To download artifacts (automatic)

## 📝 Customization

### Change Python Version

Edit in both workflow files:

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # Change this
```

### Add More Platforms

You can add ARM builds, older Windows versions, etc.:

```yaml
build-linux-arm:
  runs-on: ubuntu-latest
  steps:
    # ... ARM-specific build steps
```

### Modify Release Notes

Edit the `body:` section in `build-releases.yml`:

```yaml
- name: Create Release
  uses: softprops/action-gh-release@v2
  with:
    body: |
      ## Your custom release notes here
```

## 📊 Workflow Visualization

```
Push v1.0.0 tag
    ↓
GitHub Actions Triggered
    ↓
    ├─→ Build Linux   (Ubuntu runner)
    ├─→ Build Windows (Windows runner)
    └─→ Build macOS   (macOS runner)
    ↓
All builds complete
    ↓
Create archives
    ↓
Upload to GitHub Release
    ↓
Release published! 🎉
```

## 🎯 Best Practices

1. **Test before tagging**: Always push to main first and check test-build workflow
2. **Semantic versioning**: Use `v1.0.0`, `v1.1.0`, `v2.0.0` format
3. **Changelog**: Keep a CHANGELOG.md for each release
4. **Pre-releases**: Use `v1.0.0-beta` for beta versions
5. **Clean commits**: Make sure main branch is clean before creating release

## 🔗 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Releases Guide](https://docs.github.com/en/repositories/releasing-projects-on-github)

## 💡 Tips

- **Download test builds**: Use test-build workflow artifacts to test before releasing
- **Manual approval**: Set `draft: true` in release workflow for manual review
- **Pre-releases**: Add `prerelease: true` for beta/alpha versions
- **Multiple tags**: You can have multiple releases for different versions
