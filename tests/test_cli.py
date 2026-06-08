from pathlib import Path
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

def test_cli_check_landing_contract_missing_catalog_path() -> None:
    result = runner.invoke(app, [
        "check", "landing",
        "--dataset", "meteocat-weather",
        "--resource", "stations-metadata",
        "--input-path", "examples/landing/stations-metadata.json",
        "--use-contract"
    ])
    assert result.exit_code == 1
    assert "catalog-path is required when --use-contract is enabled" in result.output

def test_cli_check_landing_contract_pass(tmp_path: Path) -> None:
    # Setup mock catalog
    catalog = tmp_path / "catalog"
    dataset_path = catalog / "datasets" / "weather" / "meteocat"
    contracts_path = dataset_path / "contracts"
    schemas_path = dataset_path / "schemas"
    contracts_path.mkdir(parents=True)
    schemas_path.mkdir(parents=True)

    contract_data = {
        "contract_id": "test-contract",
        "dataset_id": "meteocat-weather",
        "source": "meteocat",
        "resource": "stations-metadata",
        "layer": "landing",
        "status": "draft",
        "validation_level": "permissive",
        "schema_ref": "./schemas/stations-metadata.schema.json"
    }
    with open(contracts_path / "stations-metadata.contract.json", "w") as f:
        import json
        json.dump(contract_data, f)

    schema_data = {"type": "object"}
    with open(schemas_path / "stations-metadata.schema.json", "w") as f:
        json.dump(schema_data, f)

    # Use a dummy payload that matches "type": "object"
    dummy_input = tmp_path / "dummy_input.json"
    with open(dummy_input, "w") as f:
        json.dump({"key": "value"}, f)

    result = runner.invoke(app, [
        "check", "landing",
        "--dataset", "meteocat-weather",
        "--resource", "stations-metadata",
        "--input-path", str(dummy_input),
        "--catalog-path", str(catalog),
        "--use-contract"
    ])
    if result.exit_code != 0:
        print(result.output)
    assert result.exit_code == 0
    assert "PASSED" in result.output
    assert "schema_validation" in result.output

def test_cli_check_landing_contract_fail(tmp_path: Path) -> None:
    # Setup mock catalog
    catalog = tmp_path / "catalog"
    dataset_path = catalog / "datasets" / "weather" / "meteocat"
    contracts_path = dataset_path / "contracts"
    schemas_path = dataset_path / "schemas"
    contracts_path.mkdir(parents=True)
    schemas_path.mkdir(parents=True)

    contract_data = {
        "contract_id": "test-contract",
        "dataset_id": "meteocat-weather",
        "source": "meteocat",
        "resource": "stations-metadata",
        "layer": "landing",
        "status": "draft",
        "validation_level": "permissive",
        "schema_ref": "./schemas/stations-metadata.schema.json"
    }
    with open(contracts_path / "stations-metadata.contract.json", "w") as f:
        import json
        json.dump(contract_data, f)

    # Schema that requires a property that is missing in the example
    schema_data = {"type": "object", "required": ["non_existent_property"]}
    with open(schemas_path / "stations-metadata.schema.json", "w") as f:
        json.dump(schema_data, f)

    # Use a dummy payload that misses the required property
    dummy_input = tmp_path / "dummy_input_fail.json"
    with open(dummy_input, "w") as f:
        json.dump({"key": "value"}, f)

    result = runner.invoke(app, [
        "check", "landing",
        "--dataset", "meteocat-weather",
        "--resource", "stations-metadata",
        "--input-path", str(dummy_input),
        "--catalog-path", str(catalog),
        "--use-contract"
    ])
    assert result.exit_code == 1
    assert "FAILED" in result.output
    assert "Payload does not match schema" in result.output
