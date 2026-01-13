# Release Notes - v0.2.0

## What's New in v0.2.0

### New Features

1. **Cleanup Utility** (`cleanup.py`)
   - Automatically fixes common Dataform compilation issues
   - Removes `database:` references from config blocks
   - Removes `database:` from `ref()` function calls
   - Replaces constant references (e.g., `wwim_utils.REFINED_WWIM`) with actual values
   - Cleans up dependencies.js files

2. **Enhanced Documentation**
   - Comprehensive troubleshooting guide
   - Python API examples
   - Common issues and solutions
   - Step-by-step publishing guide

3. **Improved Package Structure**
   - Moved cleanup utilities to main package
   - Excluded example-project from distribution
   - Better organization of utilities

### Bug Fixes

- Fixed handling of JSON reports with log lines
- Improved error messages for missing files
- Better handling of nested config blocks

### Documentation Updates

- Added detailed README with troubleshooting
- Updated README_PACKAGE.md for PyPI
- Created comprehensive PUBLISHING.md guide
- Added usage examples and common patterns

## Migration Guide

### From v0.1.0 to v0.2.0

No breaking changes! The upgrade is backward compatible.

**New recommended workflow:**

```bash
# 1. Generate JSON report
dataform compile --json > dependencies_report.txt

# 2. Convert to text format (NEW)
poetry run python -m dataform_viz.dataform_check > dependencies_text_report.txt

# 3. Generate diagrams
dataform-deps --report dependencies_text_report.txt generate-all
dataform-deps --report dependencies_text_report.txt index
```

**Optional cleanup (NEW):**

```bash
# Fix common Dataform issues
python -m dataform_viz.dataform_check --cleanup
```

## Files Changed

### Added
- `src/dataform_viz/cleanup.py` - Cleanup utility module
- `RELEASE_NOTES.md` - This file

### Modified
- `README.md` - Enhanced with troubleshooting and examples
- `README_PACKAGE.md` - Updated for PyPI publication
- `PUBLISHING.md` - Complete publishing guide
- `pyproject.toml` - Version bump to 0.2.0
- `.gitignore` - Added example-project exclusion

### Removed
- None (backward compatible)

## Installation

```bash
# New installation
pip install dataform-dependency-visualizer==0.2.0

# Upgrade from 0.1.0
pip install --upgrade dataform-dependency-visualizer
```

## Testing

All tests passing:
- ✅ Parser tests
- ✅ SVG generator tests
- ✅ Dataform check tests
- ✅ Integration tests

## Known Issues

None currently. Please report issues at:
https://github.com/OshigeAkito/dataform-dependency-visualizer/issues

## Credits

Special thanks to all contributors and users who provided feedback!

## Next Steps

After upgrading:

1. Run cleanup utility if you have Dataform compilation issues
2. Regenerate your diagrams to get the latest improvements
3. Check out the new troubleshooting guide in README.md

## Links

- **GitHub**: https://github.com/OshigeAkito/dataform-dependency-visualizer
- **PyPI**: https://pypi.org/project/dataform-dependency-visualizer/
- **Documentation**: See README.md
- **Issues**: https://github.com/OshigeAkito/dataform-dependency-visualizer/issues
