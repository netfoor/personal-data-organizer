import typer
from .inventory import build_catalog_step1
from pathlib import Path

app = typer.Typer(help="Personal Data Organizer CLI")

@app.command()
def inventory(root: Path = typer.Argument(..., help="Root directory to scan")):
    """Scan files under ROOT and print a quick summary."""
    build_catalog_step1(root)

if __name__ == "__main__":
    app()
