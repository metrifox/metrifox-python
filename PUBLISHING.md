# Publishing Guide for Metrifox SDK

## Quick Reference

### Test on TestPyPI (Recommended first!)
```bash
python3 -m twine upload --repository testpypi dist/*
```

Then test install:
```bash
pip install --index-url https://test.pypi.org/simple/ metrifox-sdk
```

### Publish to Production PyPI
```bash
python3 -m twine upload dist/*
```

Then anyone can install with:
```bash
pip install metrifox-sdk
```

## Complete Publishing Workflow

### 1. Prepare for Publishing

**Update version** in `pyproject.toml` (line 7):
```toml
version = "1.0.1"  # Increment for each release
```

**Build the package:**
```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build new distribution
python3 -m build
```

### 2. Test Upload to TestPyPI

Upload:
```bash
python3 -m twine upload --repository testpypi dist/*
```

You'll be prompted for:
- Username: Your TestPyPI username
- Password: Your TestPyPI password or token

Test installation:
```bash
# Create a test virtualenv
python3 -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ metrifox-sdk

# Test it
python3 -c "from metrifox_sdk import MetrifoxClient; print('Success!')"

# Cleanup
deactivate
rm -rf test_env
```

### 3. Publish to Production PyPI

Once you've verified everything works on TestPyPI:

```bash
python3 -m twine upload dist/*
```

You'll be prompted for:
- Username: Your PyPI username
- Password: Your PyPI password or token

### 4. Verify Installation

```bash
pip install metrifox-sdk
```

## Using API Tokens (Recommended)

Instead of passwords, use API tokens for better security:

1. **Create TestPyPI token**: https://test.pypi.org/manage/account/token/
2. **Create PyPI token**: https://pypi.org/manage/account/token/

Configure in `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc... # Your PyPI token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZw... # Your TestPyPI token
```

Then upload without prompts:
```bash
# TestPyPI
python3 -m twine upload --repository testpypi dist/*

# PyPI
python3 -m twine upload dist/*
```

## Releasing New Versions

1. **Update CHANGELOG.md** with changes
2. **Bump version** in `pyproject.toml`
3. **Commit changes**:
   ```bash
   git add .
   git commit -m "Bump version to X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```
4. **Clean and rebuild**:
   ```bash
   rm -rf dist/ build/ *.egg-info
   python3 -m build
   ```
5. **Upload to PyPI**:
   ```bash
   python3 -m twine upload dist/*
   ```

## Troubleshooting

### "File already exists"
You can't re-upload the same version. Increment the version number.

### Import errors after installation
Make sure you're not in the SDK directory when testing. Python may import the local files instead of the installed package.

### Missing dependencies
Verify `dependencies` in `pyproject.toml` includes all required packages.

## Security Best Practices

- ✅ Use API tokens instead of passwords
- ✅ Enable 2FA on your PyPI account
- ✅ Use project-scoped tokens when possible
- ✅ Never commit tokens to git
- ✅ Test on TestPyPI before publishing to PyPI
