import typer

app = typer.Typer(help="Personal Data Organizer CLI")

@app.command()
def inventory(root: str):
    """
    Scan files under ROOT and output a catalog (to artifacts/).
    """
    typer.echo(f"Inventorying files under: {root}")

if __name__ == "__main__":
    app()
