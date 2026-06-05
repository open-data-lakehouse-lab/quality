from pathlib import Path
from odl_quality.models.result import QualityCheckResult, QualityReport
from odl_quality.readers.jsonl_reader import read_jsonl
from odl_quality.validation.resources import validate_entity

SILVER_REQUIRED_FIELDS = [
    "dataset_id",
    "source",
    "entity",
    "attributes",
    "source_payload",
    "processing_metadata",
]

def check_silver(dataset: str, entity: str, input_path: Path) -> QualityReport:
    """Run silver quality checks."""
    results = []
    
    # Check entity support
    try:
        validate_entity(entity)
        results.append(QualityCheckResult(
            check_name="entity_supported",
            passed=True,
            message=f"Entity {entity} is supported"
        ))
    except ValueError as e:
        results.append(QualityCheckResult(
            check_name="entity_supported",
            passed=False,
            message=str(e)
        ))
        return QualityReport(dataset=dataset, resource=entity, results=results)

    # Check file exists
    file_exists = input_path.exists()
    results.append(QualityCheckResult(
        check_name="file_exists",
        passed=file_exists,
        message=f"File exists: {input_path}" if file_exists else f"File not found: {input_path}"
    ))
    
    if not file_exists:
        return QualityReport(dataset=dataset, resource=entity, results=results)

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
            all_match_entity = True
            missing_info = []
            mismatch_info = []
            
            for i, rec in enumerate(records):
                # Minimal fields
                missing = [f for f in SILVER_REQUIRED_FIELDS if f not in rec]
                if missing:
                    all_have_fields = False
                    missing_info.append(f"Record {i} missing: {', '.join(missing)}")
                
                # Entity match
                if "entity" in rec and rec["entity"] != entity:
                    all_match_entity = False
                    mismatch_info.append(f"Record {i} entity mismatch: expected {entity}, found {rec['entity']}")
            
            results.append(QualityCheckResult(
                check_name="minimal_silver_structure",
                passed=all_have_fields,
                message="All records have minimal silver structure" if all_have_fields else f"Some records missing fields: {missing_info[:1]}"
            ))
            
            results.append(QualityCheckResult(
                check_name="entity_match",
                passed=all_match_entity,
                message=f"All records match entity {entity}" if all_match_entity else f"Some records entity mismatch: {mismatch_info[:1]}"
            ))
            
    except Exception as e:
        results.append(QualityCheckResult(
            check_name="valid_jsonl",
            passed=False,
            message=f"Failed to parse JSONL: {e}"
        ))

    return QualityReport(dataset=dataset, resource=entity, results=results)
