from pathlib import Path
import typer
from odl_quality.checks.landing import check_landing
from odl_quality.checks.bronze import check_bronze
from odl_quality.reports.console import print_report

app = typer.Typer(help="ODL Quality CLI")

@app.command()
def version() -> None:
    """Show the version."""
    typer.echo("odl-quality version 0.1.0")

@app.command()
def check(
    stage: str = typer.Argument(..., help="Stage to check (landing, bronze)"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    resource: str = typer.Option(..., "--resource", help="Resource name"),
    input_path: Path = typer.Option(..., "--input-path", help="Path to the input file"),
) -> None:
    """Run quality checks for a specific stage."""
    if stage == "landing":
        report = check_landing(dataset, resource, input_path)
    elif stage == "bronze":
        report = check_bronze(dataset, resource, input_path)
    else:
        typer.echo(f"Error: Unsupported stage '{stage}'")
        raise typer.Exit(code=1)
    
    print_report(report)
    
    if not report.passed:
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
