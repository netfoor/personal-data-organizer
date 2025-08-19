setup:
	uv sync
	uv run pre-commit install

lint:
	uv run ruff check src tests

typecheck:
	uv run mypy src

test:
	uv run pytest -v

run:
	uv run pdo --help
