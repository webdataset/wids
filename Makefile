.PHONY: venv shell test docs serve lint push pypi clean testpypi rerelease patchrelease minorrelease majorrelease

# Lint code using Black and Ruff
lint:
	uv run black .
	uv run isort .
	uv run ruff check .

autofix:
	uv run ruff check --fix .

# Create virtual environment and install dependencies using uv
venv:
	type uv  # uv must be installed
	python -m venv .venv
	uv sync --all-extras
	. .venv/bin/activate && pip install -e .

# Clean up virtual environment and cache
clean:
	rm -rf .venv
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	find . -type d -name __pycache__ -exec rm -rf {} +

# Run tests using pytest
test:
	uv run pytest

# Generate documentation using MkDocs
docs:
	# jupyter-nbconvert readme.ipynb --to markdown && mv readme.md README.md
	uv run mkdocs build

# Serve documentation locally (for preview)
serve:
	uv run mkdocs serve

# Stage, commit, and push changes to GitHub
push:
	git add .
	git push

# Build and upload to TestPyPI
testpypi:
	uv run python -m build
	uv run twine upload --repository testpypi dist/*
	@echo "Install with: pip install --index-url https://test.pypi.org/simple/ --no-deps PACKAGE"

# Rebuild and reupload current version
release:
	git push
	test -z "$$(git status --porcelain)"
	uv run python -m build
	uv run twine upload "$$(ls -t dist/*.whl | sed 1q)"
	uv run twine upload "$$(ls -t dist/*.tar.gz | sed 1q)"

# Patch release (0.0.x)
patch:
	bumpversion patch
	$(MAKE) release

# Minor release (0.x.0)
minorrelease:
	bumpversion minor
	$(MAKE) release

# Major release (x.0.0)
majorrelease:
	bumpversion major
	$(MAKE) release
