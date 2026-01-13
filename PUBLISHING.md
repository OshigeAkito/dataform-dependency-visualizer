# Publishing to PyPI

This guide explains how to publish the `dataform-dependency-visualizer` package to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on both [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)
2. **API Tokens**: Generate API tokens from your account settings
3. **Poetry**: Ensure Poetry is installed and configured

## Setup PyPI Credentials

### Option 1: Using Poetry Config (Recommended)

```bash
# Configure PyPI token
poetry config pypi-token.pypi your-api-token-here

# Configure TestPyPI token (optional, for testing)
poetry config pypi-token.testpypi your-test-api-token-here
```

### Option 2: Using Environment Variables

```bash
# Windows PowerShell
$env:POETRY_PYPI_TOKEN_PYPI = "your-api-token-here"
$env:POETRY_PYPI_TOKEN_TESTPYPI = "your-test-api-token-here"

# Linux/Mac
export POETRY_PYPI_TOKEN_PYPI="your-api-token-here"
export POETRY_PYPI_TOKEN_TESTPYPI="your-test-api-token-here"
```

## Pre-Publish Checklist

Before publishing, verify:

- [ ] Version number updated in `pyproject.toml`
- [ ] `README_PACKAGE.md` updated with latest features
- [ ] `CHANGELOG` section updated in README
- [ ] All tests passing: `poetry run pytest`
- [ ] Package builds successfully: `poetry build`
- [ ] No sensitive data in `example-project/` (it's gitignored)
- [ ] Git tag created for version: `git tag v0.2.0`

## Publishing Steps

### Step 1: Clean Previous Builds

```bash
# Remove old build artifacts
Remove-Item -Recurse -Force dist/
```

### Step 2: Update Version

Edit `pyproject.toml`:

```toml
[tool.poetry]
name = "dataform-dependency-visualizer"
version = "0.2.0"  # Update this
```

### Step 3: Build Package

```bash
# Build both wheel and source distribution
poetry build
```

This creates:
- `dist/dataform_dependency_visualizer-0.2.0-py3-none-any.whl`
- `dist/dataform_dependency_visualizer-0.2.0.tar.gz`

### Step 4: Test on TestPyPI (Optional but Recommended)

```bash
# Publish to TestPyPI
poetry publish -r testpypi

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ dataform-dependency-visualizer

# Verify it works
dataform-deps --help
```

### Step 5: Publish to PyPI

```bash
# Publish to production PyPI
poetry publish

# Or in one command (build + publish)
poetry publish --build
```

### Step 6: Verify Publication

```bash
# Check on PyPI
# Visit: https://pypi.org/project/dataform-dependency-visualizer/

# Test installation
pip install dataform-dependency-visualizer

# Verify version
pip show dataform-dependency-visualizer
```

### Step 7: Create Git Tag

```bash
# Create and push tag
git tag v0.2.0
git push origin v0.2.0

# Or create annotated tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

## Post-Publish

1. **GitHub Release**: Create a release on GitHub with the tag
2. **Announcement**: Update project documentation
3. **Monitor**: Watch for issues on GitHub

## Troubleshooting

### Authentication Errors

If you see authentication errors:

```bash
# Re-configure token
poetry config pypi-token.pypi your-new-token

# Or use username/password (not recommended)
poetry publish -u username -p password
```

### Version Already Exists

You cannot republish the same version. Either:

1. Increment version in `pyproject.toml`
2. Delete the release on PyPI (only possible within 24 hours)

### Package Too Large

If package exceeds size limit:

1. Check `.gitignore` and `example-project/` is excluded
2. Verify no large files in `dist/` build
3. Use `.gitattributes` to exclude test files

## Versioning Strategy

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.2.0): New features, backward compatible
- **PATCH** (0.2.1): Bug fixes, backward compatible

Example version bumps:

```bash
# Patch release (bug fixes)
poetry version patch  # 0.2.0 -> 0.2.1

# Minor release (new features)
poetry version minor  # 0.2.0 -> 0.3.0

# Major release (breaking changes)
poetry version major  # 0.2.0 -> 1.0.0
```

## Complete Workflow Example

```bash
# 1. Make your changes
git add .
git commit -m "Add new feature"

# 2. Update version
poetry version minor  # Updates pyproject.toml

# 3. Update CHANGELOG in README.md
# Edit README.md and add new version entry

# 4. Clean and build
Remove-Item -Recurse -Force dist/
poetry build

# 5. Test on TestPyPI
poetry publish -r testpypi
pip install --index-url https://test.pypi.org/simple/ dataform-dependency-visualizer

# 6. Publish to PyPI
poetry publish

# 7. Tag release
$version = (poetry version -s)
git tag "v$version"
git push origin "v$version"

# 8. Push changes
git push origin main
```

## Additional Resources

- [Poetry Publishing Docs](https://python-poetry.org/docs/cli/#publish)
- [PyPI Help](https://pypi.org/help/)
- [TestPyPI](https://test.pypi.org/)
- [Semantic Versioning](https://semver.org/)

## Security Notes

- **Never commit API tokens** to version control
- Use `.env` files for local development (add to `.gitignore`)
- Rotate tokens regularly
- Use scoped tokens when possible (PyPI supports project-specific tokens)

## Package Statistics

After publishing, you can track:

- **Downloads**: https://pypistats.org/packages/dataform-dependency-visualizer
- **GitHub Stars**: Monitor repository popularity
- **Issues**: Track user feedback and bug reports

## Steps to Publish

### 1. Update package details

Edit `pyproject.toml`:
- Update `name`, `version`, `authors`, `email`
- Update `Homepage` and `Repository` URLs

### 2. Build the package

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build
```

This creates:
- `dist/dataform_dependency_visualizer-0.1.0-py3-none-any.whl`
- `dist/dataform-dependency-visualizer-0.1.0.tar.gz`

### 3. Test on TestPyPI (recommended)

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ dataform-dependency-visualizer
```

### 4. Upload to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
```

You'll need PyPI credentials. Create account at:
- https://pypi.org/account/register/

### 5. Verify installation

```bash
pip install dataform-dependency-visualizer
dataform-deps --help
```

## Before Publishing

- [ ] Update version in `pyproject.toml`
- [ ] Update `README_PACKAGE.md` with real examples
- [ ] Add your name/email in `pyproject.toml`
- [ ] Test locally: `pip install -e .`
- [ ] Test all CLI commands
- [ ] Add GitHub repo URL
- [ ] Review LICENSE (currently MIT)
- [ ] Write CHANGELOG.md

## Package Structure

```
wwim/
├── pyproject.toml          # Package metadata
├── LICENSE                 # MIT License
├── README_PACKAGE.md       # PyPI documentation
├── src/
│   └── dataform_viz/       # Main package
│       ├── __init__.py     # Package exports
│       ├── cli.py          # CLI entry point
│       ├── parser.py       # Report parser
│       ├── visualizer.py   # Main visualizer class
│       ├── svg_generator.py    # SVG generation
│       ├── master_index.py     # Index generation
│       └── dataform_check.py   # Prerequisites check
└── dist/                   # Built distributions (after build)
```

## Version Numbering

Follow semantic versioning (semver):
- `0.1.0` - Initial release
- `0.1.1` - Bug fixes
- `0.2.0` - New features (backward compatible)
- `1.0.0` - Stable API

## Useful Commands

```bash
# Install in development mode
pip install -e .

# Run without installing
python -m dataform_viz.cli generate dashboard_wwim

# Check package metadata
python -m build --sdist --wheel
twine check dist/*

# Clean build artifacts
rm -rf dist/ build/ *.egg-info
```
