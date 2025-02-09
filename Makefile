.PHONY: venv shell test docs serve lint push pypi

# Lint code using Black and Ruff
lint:
	poetry run black .
	poetry run isort .
	poetry run ruff check .

# Create virtual environment and install dependencies (using Poetry)
venv:
	poetry install
	rm -f .venv
	ln -s $(shell poetry env info --path) .venv

# Create virtual environment and install dependencies (using Poetry)
clean:
	rm -rf .venv
	rm -rf poetry.lock
	poetry env remove $(poetry env info --path)


# Activate the virtual environment (starts an interactive shell)
shell:
	poetry shell

# Run tests using pytest
test:
	poetry run pytest

# Generate documentation using MkDocs
docs:
	poetry run mkdocs build

# Serve documentation locally (for preview)
serve:
	poetry run mkdocs serve

# Stage, commit, and push changes to GitHub
push:
	git add .
	git push

# Build the package and publish to PyPI manually
pypi:
	poetry build
	twine upload dist/*

# Bump version (patch), commit, tag, and push release to GitHub
# release:
# 	poetry run bump2version patch
# 	git push
# 	git push --tags
