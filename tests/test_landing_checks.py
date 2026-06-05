import json
from pathlib import Path
from odl_quality.checks.landing import check_landing

def test_landing_checks_valid(tmp_path: Path) -> None:
    p = tmp_path / "valid.json"
    p.write_text(json.dumps([{"id": 1}]))
    
    report = check_landing("dataset", "stations-metadata", p)
    assert report.passed
    assert any(r.check_name == "valid_json" and r.passed for r in report.results)

def test_landing_checks_missing_file() -> None:
    report = check_landing("dataset", "stations-metadata", Path("non_existent.json"))
    assert not report.passed
    assert any(r.check_name == "file_exists" and not r.passed for r in report.results)

def test_landing_checks_empty_json(tmp_path: Path) -> None:
    p = tmp_path / "empty.json"
    p.write_text("{}")
    
    report = check_landing("dataset", "stations-metadata", p)
    assert not report.passed
    assert any(r.check_name == "not_empty" and not r.passed for r in report.results)

def test_landing_checks_unsupported_resource(tmp_path: Path) -> None:
    p = tmp_path / "valid.json"
    p.write_text(json.dumps([{"id": 1}]))
    
    report = check_landing("dataset", "unknown-resource", p)
    assert not report.passed
    assert any(r.check_name == "resource_supported" and not r.passed for r in report.results)
