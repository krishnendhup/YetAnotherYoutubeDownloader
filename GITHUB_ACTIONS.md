# GitHub Actions Workflows

This project uses GitHub Actions to automatically build and release executables for Windows, macOS, and Linux.

## Workflows

### 1. Build & Release (`build.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Push to tags matching `v*` (e.g., `v1.0.0`)
- Manual trigger via workflow dispatch

**Jobs:**
1. **Test** - Verifies code syntax and imports
2. **Build Linux** - Creates Linux executable
3. **Build Windows** - Creates Windows .exe
4. **Build macOS** - Creates macOS .dmg
5. **Release** - Creates GitHub release (only on version tags)

### 2. Tests (`test.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

**Checks:**
- Python syntax validation
- Linting with flake8
- Import availability
- Dependency compatibility

## How to Use

### Automatic Releases (Recommended)

1. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Feature: add new feature"
   git push origin main
   ```

2. **Create a release tag:**
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

3. **GitHub Actions will:**
   - ✅ Run tests
   - ✅ Build for all platforms
   - ✅ Create a release with all artifacts
   - ✅ Attach .exe, .dmg, and Linux executable

### Manual Builds

If you want to build without creating a release:

1. Go to: **Actions** → **Build & Release**
2. Click **Run workflow**
3. Choose branch and click **Run workflow**
4. Download artifacts from the workflow run

## Testing Locally with `act`

### Install `act`

**macOS:**
```bash
brew install act
```

**Windows:**
```bash
choco install act-cli
```

**Linux:**
```bash
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash
```

### Test Workflows Locally

**Run all workflows:**
```bash
act
```

**Run specific workflow:**
```bash
act -W .github/workflows/build.yml
```

**Run specific job:**
```bash
act -j build-linux
```

**Test with verbose output:**
```bash
act -v
```

**Simulate a tag push:**
```bash
act -e tag-event.json
```

Where `tag-event.json` contains:
```json
{
  "ref": "refs/tags/v1.0.0",
  "event": "push"
}
```

## Release Checklist

Before creating a release:

- [ ] All tests passing locally (`python -m pytest` or `python -m py_compile main.py`)
- [ ] Update version in `setup.py`
- [ ] Update CHANGELOG or commit message with release notes
- [ ] Test the build locally: `python build.py`
- [ ] Commit all changes
- [ ] Create tag: `git tag v1.0.0`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Wait for GitHub Actions to complete
- [ ] Verify release on GitHub Releases page

## GitHub Secrets (Optional)

If you need to add secrets for code signing or uploads:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add your secrets (e.g., `SIGNING_KEY`, `DEPLOYMENT_TOKEN`)

Then use in workflows:
```yaml
- name: Use secret
  run: echo ${{ secrets.MY_SECRET }}
```

## Troubleshooting

### Build fails locally with `act`

**Issue:** "Docker not running"
- Start Docker Desktop and try again

**Issue:** "Image pull failed"
- Run: `act --pull always`

### Release not created

**Check:**
1. Did you push a tag starting with `v`? (e.g., `v1.0.0`)
2. Are all build jobs passing?
3. Check Actions tab for workflow errors

### Artifacts not found

**Issue:** Build succeeded but artifacts are missing
- Check build step outputs
- Verify file paths in build.yml match actual output

**Solution:** Run build locally to test
```bash
python build.py
ls -la dist/
```

## Customizing Workflows

### Add Code Signing (macOS)

```yaml
- name: Sign macOS App
  run: |
    codesign --deep --force --verbose --sign - dist/YouTube-Downloader.app
```

### Add Notarization (macOS)

```yaml
- name: Notarize macOS App
  run: |
    xcrun notarytool submit dist/YouTube-Downloader.dmg \
      --apple-id ${{ secrets.APPLE_ID }} \
      --password ${{ secrets.APPLE_PASSWORD }}
```

### Add Windows Code Signing

```yaml
- name: Sign Windows Executable
  run: |
    signtool sign /f cert.pfx /p ${{ secrets.CERT_PASSWORD }} \
      dist/YouTube-Downloader.exe
```

## Performance Tips

- **Cache pip dependencies** - Already configured (saves ~30 seconds)
- **Parallel builds** - Matrix strategy runs all platforms simultaneously
- **Artifact retention** - Set to 7 days (configurable)

## More Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [act - GitHub Actions Simulator](https://github.com/nektos/act)
