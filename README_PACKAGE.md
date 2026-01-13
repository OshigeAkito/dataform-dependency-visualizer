# Dataform Dependency Visualizer

Generate beautiful, interactive SVG diagrams showing dependencies between Dataform tables.

![PyPI](https://img.shields.io/pypi/v/dataform-dependency-visualizer)
![Python](https://img.shields.io/pypi/pyversions/dataform-dependency-visualizer)
![License](https://img.shields.io/pypi/l/dataform-dependency-visualizer)

## Features

- 📊 **Interactive SVG Diagrams** - One diagram per table showing all dependencies
- 🎨 **Color-Coded by Type** - Tables, views, and operations visually distinct
- 🔍 **Master Index** - Browse all tables in a single HTML interface
- 📁 **Schema Organization** - Automatically organized by database schema
- ⚡ **Pure Python** - No Graphviz required, pure SVG generation
- 🎯 **Smart Layout** - Clean orthogonal routing for professional diagrams
- 📝 **Text Wrapping** - Long table names automatically wrapped
- 🧹 **Cleanup Utilities** - Built-in tools to fix common Dataform issues

## Installation

```bash
pip install dataform-dependency-visualizer
```

## Prerequisites

You need **Dataform CLI** installed:

```bash
# Install globally
npm install -g @dataform/cli

# Or in your project
npm install @dataform/core
```

## Quick Start

1. **Generate dependency report** from your Dataform project:

```bash
cd your-dataform-project
dataform compile --json > dependencies_report.txt
```

2. **Convert to text format** for visualization:

```bash
poetry run python -m dataform_viz.dataform_check > dependencies_text_report.txt
```

3. **Generate diagrams**:

```bash
# For all schemas
dataform-deps --report dependencies_text_report.txt generate-all

# For specific schema
dataform-deps --report dependencies_text_report.txt generate dashboard

# Generate browsable index
dataform-deps --report dependencies_text_report.txt index
```

4. **View results**: Open `output/dependencies_master_index.html` in your browser

## Command Reference

```bash
# Generate for specific schema
dataform-deps --report FILE generate SCHEMA_NAME

# Generate all schemas
dataform-deps --report FILE generate-all

# Generate master index
dataform-deps --report FILE index

# Open index in browser
dataform-deps --report FILE index --open

# Custom output directory
dataform-deps --report FILE --output my_output generate-all

# Cleanup Dataform issues
python -m dataform_viz.dataform_check --cleanup
```

## Python API

```python
from dataform_viz import DependencyVisualizer

# Initialize with report
viz = DependencyVisualizer('dependencies_text_report.txt')
viz.load_report()

# Generate for specific schema
count = viz.generate_schema_svgs('dashboard', output_dir='output')

# Generate for all schemas
total = viz.generate_all_svgs(output_dir='output')

# Generate master index
viz.generate_master_index('output')
```

## Output Structure

```
output/
├── dependencies_master_index.html  # Interactive browser interface
├── analytics/
│   └── analytics_customer_summary.svg
├── dashboard_wwim/
│   ├── dashboard_wwim_table1.svg
│   └── ...
└── datamart_wwim/
    └── ...
```

## Understanding the Diagrams

Each SVG shows:
- **Center (Yellow)**: The table being viewed
- **Left (Blue)**: Dependencies - tables this reads FROM
- **Right (Green)**: Dependents - tables that read FROM this
- **Schema Labels**: Shows schema for each table
- **Type Badges**: table, view, incremental, operation

## Cleanup Utilities

Fix common Dataform compilation issues:

```bash
python -m dataform_viz.dataform_check --cleanup
```

This removes:
- `database:` lines from config blocks
- `database:` from `ref()` calls
- Replaces constant references with actual values
- Cleans up dependencies.js files

## Common Issues

### "wwim_utils is not defined"

Run the cleanup utility:
```bash
python -m dataform_viz.dataform_check --cleanup
```

### Empty SVG output

Use text format report, not JSON:
```bash
python -m dataform_viz.dataform_check > dependencies_text_report.txt
```

## Requirements

- Python 3.10+
- Dataform CLI
- Node.js (to run Dataform)

## Links

- **GitHub**: [https://github.com/OshigeAkito/dataform-dependency-visualizer](https://github.com/OshigeAkito/dataform-dependency-visualizer)
- **Documentation**: [GitHub README](https://github.com/OshigeAkito/dataform-dependency-visualizer#readme)
- **Issues**: [GitHub Issues](https://github.com/OshigeAkito/dataform-dependency-visualizer/issues)

## License

MIT License - See LICENSE file for details.

## Changelog

### v0.2.0 (2026-01-13)
- Added cleanup utility for database references
- Added constant replacement functionality
- Improved error handling
- Enhanced documentation

### v0.1.0
- Initial release
- Basic SVG generation
- Master index generator
- Command-line interface
- **Color coding** - Tables (blue), views (green), operations (orange)

### Master Index

The master index organizes all tables by schema with:
- Clickable table names that open their SVG
- Expandable/collapsible schemas
- Type badges (table/view/incremental)
- Search functionality

## Requirements

- Python 3.8+
- Dataform project with compiled dependencies

## How It Works

1. Parse `dependencies_report.txt` generated by Dataform
2. Extract table dependencies and metadata
3. Generate SVG diagrams with orthogonal routing
4. Create master index HTML for easy navigation

## Project Structure

```
output/
├── dependencies_master_index.html    # Main entry point
└── dependencies/
    ├── schema1_table1.svg
    ├── schema1_table2.svg
    └── ...
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please open an issue or PR on GitHub.

## Links

- [GitHub Repository](https://github.com/OshigeAkito/dataform-dependency-visualizer)
- [Issue Tracker](https://github.com/OshigeAkito/dataform-dependency-visualizer/issues)
