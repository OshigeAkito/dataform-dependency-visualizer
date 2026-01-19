# Dataform Dependency Visualizer

Generate beautiful, interactive SVG diagrams showing dependencies between Dataform tables.

![Version](https://img.shields.io/badge/version-0.2.2-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- 📊 **Interactive SVG Diagrams** - One diagram per table showing dependencies and dependents
- 🎨 **Color-Coded Visualization** - Tables, views, and operations visually distinct
- 🔍 **Master Index** - Browse all tables in a single HTML interface
- 📁 **Schema Organization** - Automatically organized by database schema
- ⚡ **Pure Python** - No Graphviz required, pure SVG generation
- 🎯 **Smart Layout** - Clean orthogonal routing for professional diagrams
- 📝 **Text Wrapping** - Long table names automatically wrapped for readability

## Quick Start

### Installation

```bash
pip install dataform-dependency-visualizer
```

### Prerequisites

You need **Dataform CLI** installed to generate dependency reports:

```bash
# Install globally
npm install -g @dataform/cli

# Or in your Dataform project
cd your-dataform-project
npm install @dataform/core
```

### Basic Usage

1. **Generate dependency report** from your Dataform project:

```bash
cd your-dataform-project
dataform compile --json > dependencies_report.txt
```

> **Note**: If you see a log line at the start of the file, that's okay - the tool handles it automatically.

2. **Generate text format** for visualization (using provided Python utility):

```bash
poetry run python -m dataform_viz.dataform_check > dependencies_text_report.txt
```

3. **Generate SVG diagrams**:

```bash
# Generate for specific schema
dataform-deps --report dependencies_text_report.txt generate <schema_name>

# Generate for all schemas
dataform-deps --report dependencies_text_report.txt generate-all

# Generate master index
dataform-deps --report dependencies_text_report.txt index
```

4. **View the results**: Open `output/dependencies_master_index.html` in your browser

## Command Reference

### Generate Diagrams

```bash
# For a specific schema
dataform-deps --report dependencies_text_report.txt generate dashboard

# For all schemas (use --exclude to skip patterns)
dataform-deps --report dependencies_text_report.txt generate-all

# With custom output directory
dataform-deps --report dependencies_text_report.txt --output my_diagrams generate-all

# Generate master index
dataform-deps --report dependencies_text_report.txt index

# Open index automatically after generation
dataform-deps --report dependencies_text_report.txt index --open
```

### Cleanup Utilities

The package includes a cleanup utility for common Dataform issues:

```bash
# Clean up database references in config blocks and ref() calls
python -m dataform_viz.dataform_check --cleanup
```

This removes:
- `database:` lines from config blocks
- `database:` parameters from `ref()` calls
- Project name variables from dependencies.js files
- Replaces constant references with actual values

## Python API

```python
from dataform_viz import DependencyVisualizer

# Initialize with report file
viz = DependencyVisualizer('dependencies_text_report.txt')

# Load the dependency graph
viz.load_report()

# Generate SVGs for a specific schema
count = viz.generate_schema_svgs(
    schema='dashboard_wwim',
    output_dir='output'
)
print(f"Generated {count} diagrams")

# Generate SVGs for all schemas
total = viz.generate_all_svgs(
    output_dir='output',
    exclude_patterns=['refined_*', 'staging_*']
)
print(f"Generated {total} total diagrams")

# Generate master index
viz.generate_master_index('output')
```

## Output Structure

After running `generate-all` and `index`, you'll have:

```
output/
├── dependencies_master_index.html  # Interactive browser interface
├── analytics/
│   ├── analytics_customer_summary.svg
│   └── ...
├── dashboard_wwim/
│   ├── dashboard_wwim_table1.svg
│   ├── dashboard_wwim_table2.svg
│   └── ...
├── datamart_wwim/
│   └── ...
└── transform_wwim/
    └── ...
```

## Understanding the Diagrams

Each SVG diagram shows:

- **📍 Center (Yellow)**: The table you're viewing
- **⬅️ Left (Blue)**: Dependencies - tables this table reads FROM
- **➡️ Right (Green)**: Dependents - tables that read FROM this table
- **🏷️ Schema Labels**: Shows which schema each table belongs to  
- **🎯 Type Badges**: Distinguishes tables, views, incremental, operations

### Example Diagram

```
┌─────────────┐          ┌──────────────────┐          ┌────────────────┐
│  staging_   │  ───────>│   dashboard_     │  ───────>│   reports_     │
│  customers  │          │   customer_      │          │   monthly      │
│  (table)    │          │   summary        │          │   (view)       │
└─────────────┘          │   (table)        │          └────────────────┘
                         └──────────────────┘
┌─────────────┐                 ↑
│  staging_   │  ───────────────┘
│  orders     │
│  (table)    │
└─────────────┘
```

## Master Index Features

The generated `dependencies_master_index.html` provides:

- **📑 Schema Sidebar**: Navigate by schema with table counts
- **🔎 Searchable**: Find tables quickly
- **📊 Statistics**: Total schemas and tables at a glance
- **🔗 Direct Links**: Click any table to view its diagram
- **📱 Responsive**: Works on desktop and mobile browsers

## Common Issues & Solutions

### Issue: "wwim_utils is not defined"

**Solution**: Run the cleanup utility to remove undefined references:

```bash
python -m dataform_viz.dataform_check --cleanup
```

### Issue: Compilation errors with `database:` in config

**Problem**: Using dynamic variables like `wwim_utils.PROJECT_ID` in config blocks

**Solution**: The cleanup utility removes these automatically. Alternatively, remove manually:

```javascript
// Before
config {
  type: "table",
  database: wwim_utils.PROJECT_ID,  // ❌ Remove this
  schema: "my_schema"
}

// After  
config {
  type: "table",
  schema: "my_schema"  // ✅ Database inherited from project config
}
```

### Issue: Empty SVG output

**Problem**: Using JSON report format instead of text format

**Solution**: Generate the text report using:

```bash
poetry run python -m dataform_viz.dataform_check > dependencies_text_report.txt
```

### Issue: Module import errors in Dataform

**Problem**: Missing `require()` statements for utility modules

**Solution**: Add at the top of your `.sqlx` files:

```javascript
const wwim_utils = require("wwim_utils");

config {
  // your config
}
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/dataform-dependency-visualizer
cd dataform-dependency-visualizer

# Install dependencies with Poetry
poetry install

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src/dataform_viz

# Format code
poetry run black src/ tests/

# Type checking
poetry run mypy src/
```

### Project Structure

```
dataform-dependency-visualizer/
├── src/
│   └── dataform_viz/
│       ├── __init__.py
│       ├── cli.py              # Command-line interface
│       ├── dataform_check.py   # Compilation & cleanup utilities
│       ├── master_index.py     # HTML index generator
│       ├── parser.py            # Dependency report parser
│       ├── svg_generator.py    # SVG diagram generation
│       └── visualizer.py       # Main orchestration
├── tests/
│   ├── test_parser.py
│   ├── test_svg_generator.py
│   └── test_dataform_check.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## Requirements

- **Python**: 3.10 or higher
- **Dataform CLI**: For generating dependency reports
- **Node.js**: Required to run Dataform CLI

## Publishing to PyPI

```bash
# Build the package
poetry build

# Publish to PyPI (requires authentication)
poetry publish

# Or publish to TestPyPI first
poetry publish -r testpypi
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Changelog

### v0.2.0 (2026-01-13)

- Added cleanup utility for database references
- Added constant replacement from utils files  
- Improved error handling in compilation
- Enhanced documentation with troubleshooting guide
- Added Python API examples

### v0.1.0 (Initial Release)

- Basic SVG generation from Dataform dependencies
- Master index HTML generator
- Command-line interface
- Schema-based organization

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/dataform-dependency-visualizer/issues)
- **Documentation**: [GitHub Wiki](https://github.com/yourusername/dataform-dependency-visualizer/wiki)

## Credits

Created for visualizing complex Dataform projects with 100+ interdependent tables. Designed to help data teams understand and maintain large-scale data transformation pipelines.
