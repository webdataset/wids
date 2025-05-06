# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WIDS (WebDataset Indexed) is a high-performance library for indexed access to WebDataset format datasets. It provides random access to WebDataset files, which are tar files with specific naming conventions. This is an alternative to the streaming-based access provided by the `webdataset` library. WIDS is designed for efficient training on large-scale datasets, particularly for deep learning applications.

## Development Environment

The project uses `uv` for managing virtual environments and dependencies:

```bash
# Create virtual environment and install dependencies
make venv

# Activate virtual environment (manually run this after make venv)
source .venv/bin/activate

# Clean project
make clean
```

## Common Commands

### Testing

```bash
# Run all tests
make test
# or alternatively
uv run pytest

# Run a specific test
uv run pytest tests/test_wids.py::TestIndexedTarSamples -v

# Run all quick tests
uv run pytest -m quick

# Run tests with coverage
make coverage
# or alternatively
uv run pytest --cov=wids --cov-report=term-missing
```

### Linting and Formatting

```bash
# Run all linters (black, isort, ruff)
make lint
# or alternatively
uv run black . && uv run isort . && uv run ruff check .

# Auto-fix some linting issues
make autofix
# or alternatively
uv run ruff check --fix .
```

### Documentation

```bash
# Generate documentation
make docs

# Serve documentation locally
make serve
# or alternatively
uv run mkdocs serve

# Update README.md from the notebook
make readme

# Generate FAQ and version info
make faq
# or alternatively
uv run python3 helpers/faq.py

make versions
# or alternatively
uv run python3 helpers/versions.py

make gendocs  # Generates all documentation
```

### Releasing

```bash
# Test patch release on TestPyPI
make testpatch

# Release current version
make release

# Patch release (increment last version number)
make patch

# Minor release (increment middle version number)
make minorrelease

# Major release (increment first version number)
make majorrelease
```

## Project Structure

- Package name: wids
- Version: 0.1.11
- Python compatibility: 3.10+

- `src/wids/`: Core library implementation
  - `wids.py`: Main module containing dataset classes
  - `wids_mmtar.py`: Memory-mapped tar file implementation
  - `wids_lru.py`: LRU caching for shards
  - `wids_dl.py`: Download functionality
  - `wids_tar.py`: Basic tar file handling
  - `wids_decode.py`: Decoders for various file formats
  - `wids_index.py`: Indexing utility (provides the `widsindex` command-line tool)
  - `wids_specs.py`: Dataset specifications
  - `wids_cleanup.py`: Cleanup utilities
  - `wids_bench.py`: Benchmarking utilities
  
- `tests/`: Test suite
- `examples/`: Example notebooks and scripts
- `docs/`: Documentation source files
- `testdata/`: Test data files

## Core Components

1. **ShardListDataset**: Main dataset class that provides indexed access to WebDataset shards
2. **IndexedTarSamples**: Provides access to samples within a tar file
3. **LRUShards**: LRU cache for managing loaded shards
4. **ChunkedSampler** and **DistributedChunkedSampler**: Samplers for efficient multi-node training

## Testing Data

The project includes test data in the `testdata/` directory that is used by the test suite.

## Code Style Guidelines

- Line length: 120 characters
- Formatting: Black + isort with Black profile
- Linting: Ruff with select=["E", "F", "W", "C90"] ignoring E712, F541, C901, E741
- Docstrings: Google style (pydocstyle convention)
- Type hints: Use proper type annotations from typing module
- Imports: Use absolute imports, not relative
- Error handling: Use explicit exceptions with helpful messages
- Naming: Follow Python conventions (snake_case for functions/variables)
- Testing: Mark tests with @pytest.mark.quick for fast-running tests
- Documentation: Update docstrings when changing function behavior
- Avoid using deprecated or obsolete functions

## Code Analysis Guidelines

- When analyzing code for issues like security vulnerabilities, focus only on code in `src/wids/`
- Exclude test files (`tests/`), example notebooks, and helper utilities (`helpers/`) from security analysis
- These non-core files may contain shell commands or other practices that would be inappropriate in library code
- For security vulnerabilities like shell injection, only evaluate the actual library code