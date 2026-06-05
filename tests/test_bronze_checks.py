import json
from pathlib import Path
from odl_quality.checks.bronze import check_bronze

def test_bronze_checks_valid(tmp_path: Path) -> None:
    p = tmp_path / "valid.jsonl"
    record = {
        "dataset_id": "ds", "source": "src", "resource": "res",
        "record_type": "type", "payload": {}, "processing_metadata": {}
    }
    p.write_text(json.dumps(record) + "\n")
    
    report = check_bronze("dataset", "stations-metadata", p)
    assert report.passed
    assert any(r.check_name == "valid_jsonl" and r.passed for r in report.results)

def test_bronze_checks_missing_file() -> None:
    report = check_bronze("dataset", "stations-metadata", Path("non_existent.jsonl"))
    assert not report.passed
    assert any(r.check_name == "file_exists" and not r.passed for r in report.results)

def test_bronze_checks_invalid_jsonl(tmp_path: Path) -> None:
    p = tmp_path / "invalid.jsonl"
    p.write_text('{"a": 1}\n{invalid}')
    
    report = check_bronze("dataset", "stations-metadata", p)
    assert not report.passed
    assert any(r.check_name == "valid_jsonl" and not r.passed for r in report.results)

def test_bronze_checks_empty_jsonl(tmp_path: Path) -> None:
    p = tmp_path / "empty.jsonl"
    p.write_text("")
    
    report = check_bronze("dataset", "stations-metadata", p)
    assert not report.passed
    assert any(r.check_name == "has_records" and not r.passed for r in report.results)

def test_bronze_checks_missing_field(tmp_path: Path) -> None:
    p = tmp_path / "missing_field.jsonl"
    record = {
        "dataset_id": "ds", "source": "src", "resource": "res",
        "record_type": "type", "payload": {}
        # missing processing_metadata
    }
    p.write_text(json.dumps(record) + "\n")
    
    report = check_bronze("dataset", "stations-metadata", p)
    assert not report.passed
    assert any(r.check_name == "minimal_bronze_structure" and not r.passed for r in report.results)
