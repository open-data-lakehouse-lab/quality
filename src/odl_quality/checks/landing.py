from pathlib import Path
from typing import Optional
from odl_quality.models.result import QualityCheckResult, QualityReport
from odl_quality.readers.json_reader import read_json
from odl_quality.validation.resources import validate_resource
from odl_quality.contracts.catalog_contract_loader import CatalogContractLoader
from odl_quality.contracts.schema_validator import SchemaValidator

def check_landing(
    dataset: str, 
    resource: str, 
    input_path: Path,
    use_contract: bool = False,
    catalog_path: Optional[Path] = None
) -> QualityReport:
    """Run landing quality checks."""
    results = []
    
    # Check resource support
    try:
        validate_resource(resource)
        results.append(QualityCheckResult(
            check_name="resource_supported",
            passed=True,
            message=f"Resource {resource} is supported"
        ))
    except ValueError as e:
        results.append(QualityCheckResult(
            check_name="resource_supported",
            passed=False,
            message=str(e)
        ))
        return QualityReport(dataset=dataset, resource=resource, results=results)

    # Check file exists
    file_exists = input_path.exists()
    results.append(QualityCheckResult(
        check_name="file_exists",
        passed=file_exists,
        message=f"File exists: {input_path}" if file_exists else f"File not found: {input_path}"
    ))
    
    if not file_exists:
        return QualityReport(dataset=dataset, resource=resource, results=results)

    # Check valid JSON and not empty
    data = None
    try:
        data = read_json(input_path)
        results.append(QualityCheckResult(
            check_name="valid_json",
            passed=True,
            message="File is valid JSON"
        ))
        
        is_not_empty = bool(data)
        results.append(QualityCheckResult(
            check_name="not_empty",
            passed=is_not_empty,
            message="Payload is not empty" if is_not_empty else "Payload is empty"
        ))
    except Exception as e:
        results.append(QualityCheckResult(
            check_name="valid_json",
            passed=False,
            message=f"Failed to parse JSON: {e}"
        ))

    # Contract validation (opt-in)
    if use_contract:
        if not catalog_path:
            results.append(QualityCheckResult(
                check_name="contract_validation",
                passed=False,
                message="--catalog-path is required when --use-contract is enabled"
            ))
        else:
            try:
                loader = CatalogContractLoader(catalog_path)
                _, schema_path = loader.load_contract(dataset, resource)
                results.append(QualityCheckResult(
                    check_name="contract_found",
                    passed=True,
                    message=f"Contract and schema found in catalog for {resource}"
                ))
                
                if data is not None:
                    validator = SchemaValidator()
                    validation_result = validator.validate(data, schema_path)
                    results.append(validation_result)
                else:
                    results.append(QualityCheckResult(
                        check_name="schema_validation",
                        passed=False,
                        message="Skipping schema validation because JSON is invalid"
                    ))
            except Exception as e:
                results.append(QualityCheckResult(
                    check_name="contract_found",
                    passed=False,
                    message=f"Contract validation error: {e}"
                ))

    return QualityReport(dataset=dataset, resource=resource, results=results)
