from typer.testing import CliRunner
from odl_quality.cli import app

runner = CliRunner()

def test_cli_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "odl-quality version" in result.output

def test_cli_check_landing_pass() -> None:
    # Use the example file created earlier
    result = runner.invoke(app, [
        "check", "landing",
        "--dataset", "meteocat-weather",
        "--resource", "stations-metadata",
        "--input-path", "examples/landing/stations-metadata.json"
    ])
    assert result.exit_code == 0
    assert "PASSED" in result.output

def test_cli_check_bronze_pass() -> None:
    result = runner.invoke(app, [
        "check", "bronze",
        "--dataset", "meteocat-weather",
        "--resource", "stations-metadata",
        "--input-path", "examples/bronze/stations-metadata.jsonl"
    ])
    assert result.exit_code == 0
    assert "PASSED" in result.output

def test_cli_check_missing_file() -> None:
    result = runner.invoke(app, [
        "check", "landing",
        "--dataset", "ds",
        "--resource", "stations-metadata",
        "--input-path", "non_existent.json"
    ])
    assert result.exit_code == 1
    assert "FAILED" in result.output
    assert "File not found" in result.output

def test_cli_check_silver_pass() -> None:
    result = runner.invoke(app, [
        "check", "silver",
        "--dataset", "meteocat-weather",
        "--entity", "stations",
        "--input-path", "examples/silver/stations.jsonl"
    ])
    assert result.exit_code == 0
    assert "PASSED" in result.output

def test_cli_check_silver_missing_file() -> None:
    result = runner.invoke(app, [
        "check", "silver",
        "--dataset", "meteocat-weather",
        "--entity", "stations",
        "--input-path", "non_existent.jsonl"
    ])
    assert result.exit_code == 1
    assert "FAILED" in result.output
    assert "File not found" in result.output

def test_cli_check_silver_unsupported_entity() -> None:
    result = runner.invoke(app, [
        "check", "silver",
        "--dataset", "meteocat-weather",
        "--entity", "unknown",
        "--input-path", "examples/silver/stations.jsonl"
    ])
    assert result.exit_code == 1
    assert "Unsupported entity" in result.output
