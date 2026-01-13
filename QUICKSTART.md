# Quick Reference Guide

## Installation

```bash
pip install dataform-dependency-visualizer
```

## Basic Workflow

### 1. Generate Dependency Report

```bash
cd your-dataform-project
dataform compile --json > dependencies_report.txt
```

### 2. Convert to Text Format

```bash
poetry run python -m dataform_viz.dataform_check > dependencies_text_report.txt
```

### 3. Generate Visualizations

```bash
# Generate all diagrams
dataform-deps --report dependencies_text_report.txt generate-all

# Generate master index
dataform-deps --report dependencies_text_report.txt index

# Open in browser
dataform-deps --report dependencies_text_report.txt index --open
```

## Common Commands

```bash
# Specific schema
dataform-deps --report FILE generate SCHEMA_NAME

# Custom output directory
dataform-deps --report FILE --output my_output generate-all

# Cleanup Dataform issues
python -m dataform_viz.dataform_check --cleanup
```

## Python API

```python
from dataform_viz import DependencyVisualizer

viz = DependencyVisualizer('dependencies_text_report.txt')
viz.load_report()
viz.generate_all_svgs('output')
viz.generate_master_index('output')
```

## Troubleshooting

### "wwim_utils is not defined"
```bash
python -m dataform_viz.dataform_check --cleanup
```

### Empty diagrams
Use text format report:
```bash
python -m dataform_viz.dataform_check > dependencies_text_report.txt
```

### Module import errors
Add at top of .sqlx files:
```javascript
const wwim_utils = require("wwim_utils");
```

## File Locations

- **Input**: `dependencies_text_report.txt`
- **Output**: `output/dependencies_master_index.html`
- **Diagrams**: `output/SCHEMA_NAME/*.svg`

## Support

- **Issues**: https://github.com/OshigeAkito/dataform-dependency-visualizer/issues
- **Docs**: https://github.com/OshigeAkito/dataform-dependency-visualizer#readme
