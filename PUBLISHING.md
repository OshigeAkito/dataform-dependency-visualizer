# Publishing to PyPI

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
