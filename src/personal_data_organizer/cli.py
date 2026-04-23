import typer
from .inventory import build_catalog_step2
from pathlib import Path
from .pdf_enrichment import enrich_pdf
from .analyzers import FolderAnalyzer
from .path_utils import normalize_input_path
import pandas as pd


app = typer.Typer(help="Personal Data Organizer CLI")

@app.command()
def inventory(
    root: Path = typer.Argument(..., help="Root directory to scan"),
    output: Path = typer.Option(
        "../../artifacts/catalog.csv", help="Output file to write the catalog to"
        )
    ):
    """Scan files under ROOT and print a quick summary."""
    root = normalize_input_path(root).expanduser().resolve()
    output = normalize_input_path(output).expanduser().resolve()
    build_catalog_step2(root, output=output)

@app.command()
def enrich(
    input: Path = typer.Option("", help="Input CSV file with file paths"),
    output: Path = typer.Option("", help="Output CSV file to save enriched data")
):
    """Enrich PDF metadata from the input CSV and save to the output CSV."""
    input = normalize_input_path(input).expanduser().resolve()
    output = normalize_input_path(output).expanduser().resolve()
    enrich_pdf(input, output)

@app.command()
def analyze(
    root: Path = typer.Argument(..., help="Root directory to analyze"),
    output: Path = typer.Option("folder_analysis.csv", help="Output CSV file")
):
    """Analyze folders and generate recommendations."""
    root = normalize_input_path(root).expanduser().resolve()
    
    if not root.exists():
        typer.secho(f"❌ Path does not exist: {root}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    
    typer.echo(f"🔍 Analyzing folders in: {root}")
    
    # Get all subdirectories
    folders = [f for f in root.iterdir() if f.is_dir() and not f.name.startswith('.')]
    
    if not folders:
        typer.echo("No folders found.")
        return
    
    results = []
    
    with typer.progressbar(folders, label="Analyzing folders") as progress:
        for folder in progress:
            try:
                analyzer = FolderAnalyzer(folder)
                analysis = analyzer.analyze()
                
                results.append({
                    "path": str(analysis.path),
                    "name": analysis.path.name,
                    "size_mb": round(analysis.size / 1024 / 1024, 2),
                    "file_count": analysis.file_count,
                    "is_empty": analysis.is_empty,
                    "is_git_repo": analysis.is_git_repo,
                    "remote_url": analysis.remote_url if analysis.is_git_repo else "",
                    "has_uncommitted": analysis.has_uncommitted_changes,
                    "has_unpushed": analysis.has_unpushed_commits,
                    "has_node_modules": analysis.has_node_modules,
                    "has_venv": analysis.has_venv,
                    "has_pycache": analysis.has_pycache,
                    "has_readme": analysis.has_readme,
                    "recommendation": analysis.recommendations.value
                })
            except Exception as e:
                typer.secho(f"⚠️  Error analyzing {folder.name}: {e}", fg=typer.colors.YELLOW)
    
    # Save to CSV
    df = pd.DataFrame(results)
    output = Path(output).expanduser().resolve()
    df.to_csv(output, index=False)
    
    typer.secho(f"\n✅ Analysis complete! Report saved to: {output}", fg=typer.colors.GREEN)
    
    # Print summary
    typer.echo("\n📊 Summary by Recommendation:")
    summary = df['recommendation'].value_counts()
    for rec, count in summary.items():
        typer.echo(f"  {rec}: {count}")

if __name__ == "__main__":
    app()
