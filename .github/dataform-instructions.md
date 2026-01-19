# Dataform Dependency Visualizer Instructions

## Project Overview
Python CLI tool that generates interactive SVG dependency diagrams for Dataform BigQuery projects. Parses Dataform's compiled JSON output and creates per-table visualizations showing upstream dependencies and downstream dependents, organized by schema.

**Core workflow**: Dataform JSON → Text Parser → SVG Generator → HTML Index

## Architecture Components

### 1. Data Pipeline Flow
```
dataform compile --json → dependencies_report.txt
    ↓ (dataform_check.py)
dependencies_text_report.txt
    ↓ (parser.py)
Python dict: {table_name: {type, dependencies, dependents}}
    ↓ (svg_generator.py)
Individual SVG files per table
    ↓ (master_index.py)
HTML index with navigation
```

### 2. Module Responsibilities
- **parser.py**: Parses text report into dict structure. Handles multiple encodings (utf-8, utf-16, cp1252, latin-1).
- **svg_generator.py**: Pure Python SVG generation (no Graphviz). Uses manual node positioning with orthogonal edge routing.
- **visualizer.py**: Orchestrator class. Methods: `generate_schema_svgs()`, `generate_all_schemas()`, `generate_master_index()`.
- **master_index.py**: Generates browsable HTML interface with schema grouping and table search.
- **dataform_check.py**: Preprocessor that cleans `*_utils.PROJECT_ID` patterns from config blocks before compilation.
- **cli.py**: Argparse-based CLI with subcommands: `generate`, `generate-all`, `index`, `cleanup`.

### 3. Key Data Structures
```python
# Main data model (parser.py output)
tables = {
    "schema.table_name": {
        "type": "table|view|operation",  # From Dataform
        "dependencies": ["parent1", "parent2"],  # Upstream tables (feeds into)
        "dependents": ["child1", "child2"]  # Downstream tables (feeds from)
    }
}
```

## Development Conventions

### File Organization
- Source: `src/dataform_viz/` (package installed via Poetry)
- Tests: `tests/` with pytest fixtures
- Example: `example-project/` demonstrates typical Dataform structure
- Entry point: `dataform-deps` CLI command (defined in pyproject.toml scripts)

### SVG Generation Pattern
**Manual positioning** (not layout algorithms):
- 3-column layout: Dependencies | Center Table | Dependents
- Fixed dimensions: 200x60px nodes, 250px horizontal spacing, 80px vertical spacing
- Vertical centering: Center table at `max(left_count, 1, right_count) // 2`
- Edges: Orthogonal routing with `M/L/C` path commands for clean 90° angles
- Colors by type: Table (green), View (blue), Operation (orange)

### Text Report Format
Parser expects:
```
Table: schema.table_name (type)
  Dependencies (N):
    <- dependency1
    <- dependency2
  Dependents (N):
    -> dependent1
```

**Critical**: JSON report may have log line at top—parser handles this implicitly by regex matching only valid table blocks.

### Testing Approach
- **pytest** with temporary files
- Test parsing edge cases: empty files, multiple encodings, various table types
- Use `tempfile.mkdtemp()` for isolated test environments
- Example pattern in [test_parser.py](../tests/test_parser.py)

### Error Handling
- File encoding: Try utf-8 → utf-16 → cp1252 → latin-1 in sequence
- Missing files: Raise `FileNotFoundError` with descriptive message
- Schema not found: Raise `ValueError` with schema name
- CLI errors: Print to stderr, return non-zero exit code

## Common Development Tasks

### Adding New Cleanup Pattern
Edit `dataform_check.py`, function `clean_config_block()`:
1. Add regex pattern matching the problematic syntax
2. Use `re.sub()` with DOTALL flag for multiline blocks
3. Apply only within `config { }` blocks (not SQL queries)
4. Test with example `.sqlx` file in `example-project/`

### Modifying SVG Layout
Edit `svg_generator.py`, function `generate_svg_manual()`:
1. Adjust constants: `node_width`, `node_height`, `h_spacing`, `v_spacing`
2. Update node positioning logic (columns are left→center→right)
3. Regenerate edges in `draw_edges()` if connection points change
4. Test with multi-dependency table (e.g., 5+ upstream, 5+ downstream)

### Adding CLI Subcommand
In `cli.py`:
1. Create `cmd_<name>(args)` function following existing pattern
2. Add subparser with `subparsers.add_parser()`
3. Set `func=cmd_<name>` on parser defaults
4. Return 0 for success, 1 for errors
5. Use ✓/✗ Unicode chars for output consistency

## Running & Testing

```powershell
# Development setup (uses .venv in workspace)
poetry install
poetry shell  # Or: & .venv\Scripts\Activate.ps1

# Run CLI in dev mode
poetry run dataform-deps --report example-project/dependencies_report.txt generate-all

# Run tests
poetry run pytest tests/ -v
poetry run pytest tests/test_parser.py::TestParseDependenciesReport::test_parse_simple_table

# Generate text report from JSON (when needed)
poetry run python -m dataform_viz.dataform_check > dependencies_text_report.txt

# Publishing (see PUBLISHING.md)
poetry build
poetry publish --build
```

## Project-Specific Gotchas

1. **Schema naming**: Uses dot notation `schema.table_name`. Safe filenames replace `.` with `_`.
2. **Exclude patterns**: Default excludes `refined_*` schemas (common staging pattern). Use `--exclude` to override.
3. **Output structure**: Creates `output/dependencies_<schema>/` folders, not flat hierarchy.
4. **Master index**: Must run `index` command after `generate-all` to create HTML navigation.
5. **Dataform JSON format**: The `dataform compile --json` output is NOT directly usable—must convert via `dataform_check.py` first.
6. **Windows paths**: Use `Path` objects everywhere for cross-platform compatibility. CLI uses PowerShell (not bash).

## External Dependencies

- **Dataform CLI** (Node.js): Required for generating initial JSON report. Not included in package.
- **Python 3.10+**: Uses match/case and type hints extensively.
- **Poetry**: Package manager and build tool. Not setuptools/pip.
- **No Graphviz**: Deliberately avoids graphviz dependency—pure Python SVG generation.

## When Modifying Package

- Bump version in [pyproject.toml](../pyproject.toml) (line 3)
- Update [README.md](../README.md) and [README_PACKAGE.md](../README_PACKAGE.md) if CLI changes
- Run tests before commit: `poetry run pytest`
- Check example still works: Test with `example-project/`
- Update [RELEASE_NOTES.md](../RELEASE_NOTES.md) for user-facing changes
