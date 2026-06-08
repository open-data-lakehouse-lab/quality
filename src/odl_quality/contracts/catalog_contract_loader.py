import json
from pathlib import Path
from typing import Any, Dict, Tuple

class CatalogContractLoader:
    def __init__(self, catalog_path: Path):
        self.catalog_path = catalog_path
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"Catalog path does not exist: {self.catalog_path}")

    def load_contract(self, dataset: str, resource: str) -> Tuple[Dict[str, Any], Path]:
        """
        Load contract JSON from catalog path.
        Expected contract path from catalog-path:
        <catalog-path>/datasets/weather/meteocat/contracts/<resource>.contract.json
        """
        # For this first implementation, support only:
        # Dataset: meteocat-weather
        # Source: meteocat
        if dataset != "meteocat-weather":
            raise ValueError(f"Unsupported dataset for contract validation: {dataset}")

        # Map dataset to path components as per requirement
        # <catalog-path>/datasets/weather/meteocat/contracts/<resource>.contract.json
        contract_path = self.catalog_path / "datasets" / "weather" / "meteocat" / "contracts" / f"{resource}.contract.json"

        if not contract_path.exists():
            raise FileNotFoundError(f"Contract file not found: {contract_path}")

        try:
            with open(contract_path, "r") as f:
                contract_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid contract JSON at {contract_path}: {e}")

        self._validate_contract_fields(contract_data, dataset, resource)

        schema_ref = contract_data["schema_ref"]
        # The contract is at: <catalog-path>/datasets/weather/meteocat/contracts/<resource>.contract.json
        # The schema_ref should be resolved relative to the dataset directory:
        # <catalog-path>/datasets/weather/meteocat/
        dataset_dir = self.catalog_path / "datasets" / "weather" / "meteocat"
        
        # If schema_ref starts with ./ or ../, it should be resolved relative to the contract's parent directory?
        # No, the requirement says:
        # "This schema_ref must be resolved relative to the Meteocat dataset directory:
        # <catalog-path>/datasets/weather/meteocat/"
        
        # Strip leading ./ if present to make it easier to join with dataset_dir
        if schema_ref.startswith("./"):
            normalized_ref = schema_ref[2:]
        elif schema_ref.startswith("../"):
            normalized_ref = schema_ref[3:]
        else:
            normalized_ref = schema_ref
            
        schema_path = (dataset_dir / normalized_ref).resolve()

        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file referenced in contract not found: {schema_path}")

        return contract_data, schema_path

    def _validate_contract_fields(self, contract_data: Dict[str, Any], expected_dataset: str, expected_resource: str) -> None:
        required_fields = [
            "contract_id",
            "dataset_id",
            "source",
            "resource",
            "layer",
            "status",
            "validation_level",
            "schema_ref"
        ]
        for field in required_fields:
            if field not in contract_data:
                raise ValueError(f"Missing required contract field: {field}")

        if contract_data["dataset_id"] != expected_dataset:
            raise ValueError(f"Contract dataset_id '{contract_data['dataset_id']}' does not match expected '{expected_dataset}'")
        
        if contract_data["resource"] != expected_resource:
            raise ValueError(f"Contract resource '{contract_data['resource']}' does not match expected '{expected_resource}'")
