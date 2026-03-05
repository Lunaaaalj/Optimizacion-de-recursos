# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Optimizacion-de-recursos** is an operations research project focused on resource optimization using mathematical modeling. The project:
- Develops optimization models using **Pyomo** (Python Optimization Modeling Objects)
- Defines sets, parameters, decision variables, objective functions, and constraints
- Uses real-world data from resource management scenarios
- Produces comprehensive LaTeX reports and documentation

## Development Setup

### Virtual Environment

The project uses Python with a virtual environment located at `venv/`. To set up:

```bash
# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Key Dependencies

- **pyomo==6.9.5** - Optimization modeling framework
- **pandas==3.0.1** - Data manipulation
- **numpy==2.4.2** - Numerical computing
- **matplotlib==3.10.8** - Visualization
- **jupyter** - Interactive notebooks
- **jupyterlab** - Jupyter lab interface

## Project Structure

### Core Directories

- **data/** - Data files (raw Excel/CSV data)
  - `raw/` - Original, immutable source data
  - `processed/` - Cleaned, transformed CSV data
- **reports/** - LaTeX reports and documentation
  - `rep_1/` - Main research report (main.tex)
  - `model/` - Model specification document (main.tex)
- **notebooks/** - Data exploration and scripting
  - `data_export.py` - Script to convert Excel files to CSV
- **src/** - Production Python code (currently minimal; expand as project grows)
- **tests/** - Unit and integration tests
- **docs/** - Additional project documentation
- **models/** - Model artifacts and metadata

### Architecture Notes

The project follows a data science template structure with separation between:
- **Exploration** (notebooks/) → exploratory data analysis and script development
- **Production Code** (src/) → reusable, tested modules (currently underdeveloped; refactor notebook code here)
- **Documentation** (reports/) → LaTeX reports and model specifications
- **Data Processing** - Excel files are converted to CSV for easier processing (see `notebooks/data_export.py`)

## Common Development Tasks

### Data Processing

Convert Excel files to CSV:
```bash
# Activate environment and run from project root
source venv/bin/activate
python notebooks/data_export.py
```

This script reads raw Excel files and outputs processed CSV files to `data/processed/`.

### Working with Jupyter Notebooks

```bash
# Start JupyterLab
jupyter lab

# Start Jupyter Notebook
jupyter notebook
```

For exploration, use `notebooks/` directory. When code becomes reusable, refactor into `src/` and import it in notebooks.

### Building Reports

The LaTeX reports in `reports/rep_1/` and `reports/model/` can be compiled using a LaTeX editor or command-line tools:
```bash
# If pdflatex is available
cd reports/rep_1
pdflatex main.tex
```

### Running Tests

Tests are located in `tests/`. When test infrastructure is set up:
```bash
# If pytest is installed
pytest tests/

# Run a single test file
pytest tests/test_file.py
```

Currently, no test infrastructure is configured. Consider adding pytest to requirements.txt when implementing tests.

## Git Workflow

See CONTRIBUTING.md for detailed contribution guidelines. Key points:

- **Branch naming**: `feature/name`, `bugfix/name`, `docs/name`, `refactor/name`, `test/name`
- **Commit messages**: Use conventional format (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`)
- **Protected main branch** - All changes must go through pull requests
- **Draft PRs** - Open a draft PR immediately after first push to signal work in progress

## Important Notes

- The main modeling code is specified in LaTeX documents in `reports/model/main.tex` and currently embedded in reports rather than as executable Pyomo code
- Data export is handled by `notebooks/data_export.py` - this reads specific Excel files and produces CSV outputs
- The `src/` directory is minimal; consider refactoring common code there as the project grows
- VS Code is configured with Spanish language support (ltex.language: "es") for LaTeX spell-checking
