from pathlib import Path
from typing import Iterator
from loguru import logger
import typer
import pandas as pd
import datetime as dt 

def _iter_files(root: Path) -> Iterator[Path]:  
    """Iterate over all files in a directory and its subdirectories."""
    if not root.exists():
        logger.warning(f"Directory {root} does not exist")
        return
    for child in root.iterdir():
        if child.is_file():
            yield child
        elif child.is_dir():
            yield from _iter_files(child)


def build_catalog_step1(root: Path) -> None:
    """Step 1: Build a catalog of files under the given root directory."""
    logger.info(f"Building catalog for files under: {root}")

    root = root.expanduser().resolve()
    
    if not root.exists():
        typer.secho(f"[error] Root does not exist: {root}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    if not root.is_dir():
        typer.secho(f"[error] Root is not a directory: {root}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    

    count = 0
    sample: list[str] = []

    for file in _iter_files(root):
        count += 1
        if len(sample) < 10:
            sample.append(str(file))

    logger.info(f"Scanned {count} files under {root}")
    if sample:
        typer.echo("Sample (first 10 files):")
        for s in sample:
            typer.echo(f"  - {s}")
    else:
        typer.echo("No files found.")

def build_catalog_step2(root: Path, output: Path) -> None:
    """Step 2: Build a catalog of files under the given root directory and save it to a CSV file."""
    logger.info(f"Building catalog for files under: {root}")

    root = root.expanduser().resolve()
    output = output.expanduser().resolve()

    rows = []

    for file in _iter_files(root):
        stat = file.stat()
        rows.append({
            "path": str(file),
            "file": file.name,
            "extension": file.suffix.lower(),
            "size_bytes": stat.st_size,
            "modified": dt.datetime.fromtimestamp(stat.st_mtime)
        })

    df = pd.DataFrame(rows)
    logger.info(f"Found {len(df)} files under {root}")

    if rows:
        output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output, index=False)
        logger.info(f"Wrote catalog to {output}")
    else:
        logger.info("No files found.")
