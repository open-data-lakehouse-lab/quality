from pathlib import Path
from typing import Optional
import typer
from odl_quality.checks.landing import check_landing
from odl_quality.checks.bronze import check_bronze
from odl_quality.checks.silver import check_silver
from odl_quality.reports.console import print_report

app = typer.Typer(help="ODL Quality CLI")

@app.command()
def version() -> None:
    """Show the version."""
    typer.echo("odl-quality version 0.1.0")

@app.command()
def check(
    stage: str = typer.Argument(..., help="Stage to check (landing, bronze, silver)"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    resource: Optional[str] = typer.Option(None, "--resource", help="Resource name (for landing/bronze)"),
    entity: Optional[str] = typer.Option(None, "--entity", help="Entity name (for silver)"),
    input_path: Path = typer.Option(..., "--input-path", help="Path to the input file"),
) -> None:
    """Run quality checks for a specific stage."""
    if stage == "landing":
        if not resource:
            typer.echo("Error: --resource is required for landing stage")
            raise typer.Exit(code=1)
        report = check_landing(dataset, resource, input_path)
    elif stage == "bronze":
        if not resource:
            typer.echo("Error: --resource is required for bronze stage")
            raise typer.Exit(code=1)
        report = check_bronze(dataset, resource, input_path)
    elif stage == "silver":
        if not entity:
            typer.echo("Error: --entity is required for silver stage")
            raise typer.Exit(code=1)
        report = check_silver(dataset, entity, input_path)
    else:
        typer.echo(f"Error: Unsupported stage '{stage}'")
        raise typer.Exit(code=1)
    
    print_report(report)
    
    if not report.passed:
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
