# 🚀 Quick Release Guide

This is a simple guide to create your first release using GitHub Actions.

## ✅ Prerequisites

- All changes committed and pushed to `main` branch
- GitHub Actions workflows are in place (already done!)
- Ready to create version `v1.0.0`

## 📋 Step-by-Step Release Process

### Method 1: Using Git Command Line (Recommended)

```bash
# 1. Make sure you're on main and up to date
git checkout main
git pull origin main

# 2. Create an annotated tag
git tag -a v1.0.0 -m "First stable release - Multi-platform ROM Manager"

# 3. Push the tag to GitHub
git push origin v1.0.0
```

**That's it!** GitHub Actions will automatically:
- ✅ Build for Linux (Ubuntu runner)
- ✅ Build for Windows (Windows runner)
- ✅ Build for macOS (macOS runner)
- ✅ Create compressed archives
- ✅ Create a GitHub Release
- ✅ Upload all files to the release

### Method 2: Using GitHub Web Interface

1. Go to: https://github.com/Tonymartos/DownloaderRomsMyrientManager/releases

2. Click **"Draft a new release"** button

3. Click on **"Choose a tag"** dropdown

4. Type `v1.0.0` in the box and click **"+ Create new tag: v1.0.0 on publish"**

5. Set **Release title**: `Myrient ROM Manager v1.0.0`

6. Add optional description (or leave it, the workflow will add one)

7. Click **"Publish release"**

8. GitHub Actions will automatically build and upload files!

## 🔍 Monitor the Build

After pushing the tag or publishing the release:

1. Go to: https://github.com/Tonymartos/DownloaderRomsMyrientManager/actions

2. You'll see the workflow **"Build Multi-Platform Releases"** running

3. Click on it to see real-time progress

4. Wait ~10 minutes for all builds to complete

5. Check the **Releases** tab for your new release!

## 📦 What Will Be Created

Your release will automatically include:

### Files
- `myrient-manager-linux-x64.tar.gz` (~27 MB)
- `myrient-manager-windows-x64.zip` (~28 MB)
- `myrient-manager-macos-universal.tar.gz` (~27 MB)

### Release Notes
- Download instructions for each platform
- Quick start guide
- Security notes for macOS
- Legal disclaimer
- Links to documentation

## ✨ Test Build First (Optional but Recommended)

Before creating the official release, you can test the builds:

1. The push to `main` already triggered the test workflow

2. Go to: https://github.com/Tonymartos/DownloaderRomsMyrientManager/actions

3. Find the latest **"Build Test"** workflow

4. Once completed, scroll down to **"Artifacts"**

5. Download and test:
   - `test-linux-build`
   - `test-windows-build`
   - `test-macos-build`

6. If everything works, proceed with the release!

## 🎯 Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **v1.0.0** - First stable release
- **v1.1.0** - New features (minor update)
- **v1.0.1** - Bug fixes (patch)
- **v2.0.0** - Breaking changes (major update)
- **v1.0.0-beta** - Pre-release (beta version)

## 🐛 If Something Goes Wrong

### Build Fails

1. Check the Actions tab for error logs
2. Fix the issue in code
3. Commit and push the fix
4. Delete the failed tag (if created):
   ```bash
   git tag -d v1.0.0
   git push origin :refs/tags/v1.0.0
   ```
5. Try again with the same or new tag

### Release Created But Files Missing

1. Check if all 3 build jobs completed successfully
2. Look at the "Create Release" job logs
3. Manually upload files if needed from Actions artifacts

### Manual Trigger

If automatic trigger doesn't work:

1. Go to: https://github.com/Tonymartos/DownloaderRomsMyrientManager/actions
2. Select **"Build Multi-Platform Releases"**
3. Click **"Run workflow"**
4. Select branch: `main`
5. Click green **"Run workflow"** button

## 📝 After Release

1. ✅ Test downloads from each platform
2. ✅ Update main README.md with release link if needed
3. ✅ Announce on social media / forums
4. ✅ Monitor for issues and user feedback

## 🔄 Future Releases

For subsequent releases, just repeat the process with new version numbers:

```bash
# Version 1.1.0 (new features)
git tag -a v1.1.0 -m "Added new ROM filtering options"
git push origin v1.1.0

# Version 1.0.1 (bug fix)
git tag -a v1.0.1 -m "Fixed download progress display"
git push origin v1.0.1
```

## 💡 Pro Tips

1. **Keep a changelog**: Document changes in `CHANGELOG.md`
2. **Test locally first**: Build with `python build.py` before releasing
3. **Use pre-releases**: Tag as `v1.0.0-beta` for testing
4. **Clean tags**: Delete failed/test tags to keep repo clean
5. **Consistent naming**: Always use `vX.Y.Z` format

## 🎉 Ready to Release?

Run this command to create your first release:

```bash
git tag -a v1.0.0 -m "First stable release"
git push origin v1.0.0
```

Then watch the magic happen at:
- Actions: https://github.com/Tonymartos/DownloaderRomsMyrientManager/actions
- Releases: https://github.com/Tonymartos/DownloaderRomsMyrientManager/releases

Good luck! 🚀
