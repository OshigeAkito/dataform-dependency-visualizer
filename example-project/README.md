# Example Dataform Project

This is a minimal example Dataform project to demonstrate the dependency visualizer.

## Structure

```
example-project/
├── dataform.json              # Dataform configuration
├── package.json               # Node.js dependencies
├── definitions/               # SQL transformations
│   ├── staging_customers.sqlx
│   ├── staging_orders.sqlx
│   └── analytics_customer_summary.sqlx
└── dependencies_report.txt    # Generated dependency report
```

## Quick Start

### 1. Install dependencies

```bash
cd example-project
npm install
```

### 2. Generate dependency report

```bash
# Using Dataform CLI
dataform compile --json > dependencies_report.txt

# Or use the included sample report
```

### 3. Visualize dependencies

```bash
cd ..
pip install -e .

# Generate SVG diagrams
dataform-deps generate staging --report example-project/dependencies_report.txt
dataform-deps generate analytics --report example-project/dependencies_report.txt

# Generate master index
dataform-deps index --report example-project/dependencies_report.txt --open
```

## Expected Output

This example creates:
- **2 staging tables**: `staging_customers`, `staging_orders`
- **1 analytics view**: `analytics_customer_summary`
- **Dependency chain**: staging → analytics

The visualizer will generate:
- `output/dependencies_staging/` - 2 SVG files
- `output/dependencies_analytics/` - 1 SVG file
- `output/dependencies_master_index.html` - Interactive viewer

## Diagram Features

Each SVG shows:
- **Yellow node**: The table/view itself
- **Blue arrows**: Dependencies (← what it reads from)
- **Green arrows**: Dependents (→ what reads from it)
- **Schema labels**: At top of each box
- **Type badges**: table/view distinction
