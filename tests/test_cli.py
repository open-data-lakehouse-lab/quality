from typer.testing import CliRunner
from odl_quality.cli import app

runner = CliRunner()

def test_cli_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "odl-quality version" in result.output

def test_cli_check_landing_pass():
    # Use the example file created earlier
    result = runner.invoke(app, [
        "check", "landing",
        "--dataset", "meteocat-weather",
        "--resource", "stations-metadata",
        "--input-path", "examples/landing/stations-metadata.json"
    ])
    assert result.exit_code == 0
    assert "PASSED" in result.output

def test_cli_check_bronze_pass():
    result = runner.invoke(app, [
        "check", "bronze",
        "--dataset", "meteocat-weather",
        "--resource", "stations-metadata",
        "--input-path", "examples/bronze/stations-metadata.jsonl"
    ])
    assert result.exit_code == 0
    assert "PASSED" in result.output

def test_cli_check_missing_file():
    result = runner.invoke(app, [
        "check", "landing",
        "--dataset", "ds",
        "--resource", "stations-metadata",
        "--input-path", "non_existent.json"
    ])
    assert result.exit_code == 1
    assert "FAILED" in result.output
    assert "File not found" in result.output
