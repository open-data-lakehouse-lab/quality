from pathlib import Path
from odl_quality.models.result import QualityCheckResult, QualityReport
from odl_quality.readers.jsonl_reader import read_jsonl
from odl_quality.validation.resources import validate_resource

BRONZE_REQUIRED_FIELDS = [
    "dataset_id",
    "source",
    "resource",
    "record_type",
    "payload",
    "processing_metadata",
]

def check_bronze(dataset: str, resource: str, input_path: Path) -> QualityReport:
    """Run bronze quality checks."""
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

    # Check valid JSONL and minimal structure
    try:
        records = read_jsonl(input_path)
        results.append(QualityCheckResult(
            check_name="valid_jsonl",
            passed=True,
            message="File is valid JSONL"
        ))
        
        has_records = len(records) > 0
        results.append(QualityCheckResult(
            check_name="has_records",
            passed=has_records,
            message=f"File has {len(records)} records" if has_records else "File has no records"
        ))
        
        if has_records:
            all_have_fields = True
            missing_info = []
            for i, rec in enumerate(records):
                missing = [f for f in BRONZE_REQUIRED_FIELDS if f not in rec]
                if missing:
                    all_have_fields = False
                    missing_info.append(f"Record {i} missing: {', '.join(missing)}")
            
            results.append(QualityCheckResult(
                check_name="minimal_bronze_structure",
                passed=all_have_fields,
                message="All records have minimal bronze structure" if all_have_fields else f"Some records missing fields: {missing_info[:1]}"
            ))
            
    except Exception as e:
        results.append(QualityCheckResult(
            check_name="valid_jsonl",
            passed=False,
            message=f"Failed to parse JSONL: {e}"
        ))

    return QualityReport(dataset=dataset, resource=resource, results=results)
