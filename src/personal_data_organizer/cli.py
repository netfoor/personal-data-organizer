import typer
from .inventory import build_catalog_step2
from pathlib import Path
from .pdf_enrichment import enrich_pdf


app = typer.Typer(help="Personal Data Organizer CLI")

@app.command()
def inventory(
    root: Path = typer.Argument(..., help="Root directory to scan"),
    output: Path = typer.Option(
        "../../artifacts/catalog.csv", help="Output file to write the catalog to"
        )
    ):
    """Scan files under ROOT and print a quick summary."""
    build_catalog_step2(root, output=output)

@app.command()
def enrich(
    input: Path = typer.Option("", help="Input CSV file with file paths"),
    output: Path = typer.Option("", help="Output CSV file to save enriched data")
):
    """Enrich PDF metadata from the input CSV and save to the output CSV."""
    enrich_pdf(input, output)

if __name__ == "__main__":
    app()
