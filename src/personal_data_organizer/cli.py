import typer
from .inventory import build_catalog_step2
from pathlib import Path

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


if __name__ == "__main__":
    app()
