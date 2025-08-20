setup:
	uv sync --all-extras
	uv pip install -e .
	uv run pre-commit install

lint:
	uv run ruff check src tests

typecheck:
	uv run mypy src

test:
	uv run pytest -v

run:
	uv run python -m personal_data_organizer.cli ~\Downloads --output "C:\IA\personal-data-organizer\artifacts\downloads_enriched.csv"

query:
	uv run python -m querys.query