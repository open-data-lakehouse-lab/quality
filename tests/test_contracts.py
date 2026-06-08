import json
from pathlib import Path
import pytest
from odl_quality.contracts.catalog_contract_loader import CatalogContractLoader
from odl_quality.contracts.schema_validator import SchemaValidator

def test_contract_loader_valid(tmp_path: Path) -> None:
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
    contract_file = contracts_path / "stations-metadata.contract.json"
    with open(contract_file, "w") as f:
        json.dump(contract_data, f)

    schema_data = {"type": "object"}
    schema_file = schemas_path / "stations-metadata.schema.json"
    with open(schema_file, "w") as f:
        json.dump(schema_data, f)

    loader = CatalogContractLoader(catalog)
    loaded_contract, resolved_schema_path = loader.load_contract("meteocat-weather", "stations-metadata")

    assert loaded_contract["contract_id"] == "test-contract"
    assert resolved_schema_path == schema_file.resolve()

def test_contract_loader_schema_ref_no_prefix(tmp_path: Path) -> None:
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
        "schema_ref": "schemas/stations-metadata.schema.json"
    }
    contract_file = contracts_path / "stations-metadata.contract.json"
    with open(contract_file, "w") as f:
        json.dump(contract_data, f)

    schema_data = {"type": "object"}
    schema_file = schemas_path / "stations-metadata.schema.json"
    with open(schema_file, "w") as f:
        json.dump(schema_data, f)

    loader = CatalogContractLoader(catalog)
    loaded_contract, resolved_schema_path = loader.load_contract("meteocat-weather", "stations-metadata")

    assert resolved_schema_path == schema_file.resolve()

def test_contract_loader_schema_ref_parent_prefix(tmp_path: Path) -> None:
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
        "schema_ref": "../schemas/stations-metadata.schema.json"
    }
    contract_file = contracts_path / "stations-metadata.contract.json"
    with open(contract_file, "w") as f:
        json.dump(contract_data, f)

    schema_data = {"type": "object"}
    schema_file = schemas_path / "stations-metadata.schema.json"
    with open(schema_file, "w") as f:
        json.dump(schema_data, f)

    loader = CatalogContractLoader(catalog)
    loaded_contract, resolved_schema_path = loader.load_contract("meteocat-weather", "stations-metadata")

    assert resolved_schema_path == schema_file.resolve()

def test_contract_loader_missing_catalog() -> None:
    with pytest.raises(FileNotFoundError, match="Catalog path does not exist"):
        CatalogContractLoader(Path("/non/existent/path"))

def test_contract_loader_missing_contract(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog"
    catalog.mkdir()
    loader = CatalogContractLoader(catalog)
    with pytest.raises(FileNotFoundError, match="Contract file not found"):
        loader.load_contract("meteocat-weather", "stations-metadata")

def test_contract_loader_invalid_json(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog"
    contract_path = catalog / "datasets" / "weather" / "meteocat" / "contracts"
    contract_path.mkdir(parents=True)
    contract_file = contract_path / "stations-metadata.contract.json"
    with open(contract_file, "w") as f:
        f.write("invalid json")

    loader = CatalogContractLoader(catalog)
    with pytest.raises(ValueError, match="Invalid contract JSON"):
        loader.load_contract("meteocat-weather", "stations-metadata")

def test_contract_loader_missing_fields(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog"
    contract_path = catalog / "datasets" / "weather" / "meteocat" / "contracts"
    contract_path.mkdir(parents=True)
    contract_file = contract_path / "stations-metadata.contract.json"
    with open(contract_file, "w") as f:
        json.dump({"contract_id": "incomplete"}, f)

    loader = CatalogContractLoader(catalog)
    with pytest.raises(ValueError, match="Missing required contract field"):
        loader.load_contract("meteocat-weather", "stations-metadata")

def test_contract_loader_mismatch(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog"
    contract_path = catalog / "datasets" / "weather" / "meteocat" / "contracts"
    contract_path.mkdir(parents=True)
    contract_file = contract_path / "stations-metadata.contract.json"
    with open(contract_file, "w") as f:
        json.dump({
            "contract_id": "test",
            "dataset_id": "mismatch",
            "source": "meteocat",
            "resource": "mismatch",
            "layer": "landing",
            "status": "draft",
            "validation_level": "permissive",
            "schema_ref": "any"
        }, f)

    loader = CatalogContractLoader(catalog)
    with pytest.raises(ValueError, match="Contract dataset_id 'mismatch' does not match expected 'meteocat-weather'"):
        loader.load_contract("meteocat-weather", "stations-metadata")

def test_schema_validator_pass(tmp_path: Path) -> None:
    schema_file = tmp_path / "schema.json"
    with open(schema_file, "w") as f:
        json.dump({"type": "object", "properties": {"name": {"type": "string"}}}, f)
    
    validator = SchemaValidator()
    result = validator.validate({"name": "test"}, schema_file)
    assert result.passed is True

def test_schema_validator_fail(tmp_path: Path) -> None:
    schema_file = tmp_path / "schema.json"
    with open(schema_file, "w") as f:
        json.dump({"type": "object", "properties": {"name": {"type": "string"}}}, f)
    
    validator = SchemaValidator()
    result = validator.validate({"name": 123}, schema_file)
    assert result.passed is False
    assert "Payload does not match schema" in result.message

def test_schema_validator_missing_schema() -> None:
    validator = SchemaValidator()
    result = validator.validate({}, Path("/non/existent/schema.json"))
    assert result.passed is False
    assert "Schema file not found" in result.message

def test_schema_validator_invalid_json(tmp_path: Path) -> None:
    schema_file = tmp_path / "schema.json"
    with open(schema_file, "w") as f:
        f.write("invalid json")
    
    validator = SchemaValidator()
    result = validator.validate({}, schema_file)
    assert result.passed is False
    assert "Invalid schema JSON" in result.message
