from pathlib import Path
from odl_quality.checks.silver import check_silver

def test_silver_stations_passes(tmp_path: Path) -> None:
    path = tmp_path / "stations.jsonl"
    path.write_text(
        '{"dataset_id": "ds", "source": "src", "entity": "stations", "natural_key": "k1", "attributes": {}, "source_payload": {}, "processing_metadata": {}}\n'
    )
    report = check_silver("ds", "stations", path)
    assert report.passed

def test_silver_variables_passes(tmp_path: Path) -> None:
    path = tmp_path / "variables.jsonl"
    path.write_text(
        '{"dataset_id": "ds", "source": "src", "entity": "variables", "natural_key": "k1", "attributes": {}, "source_payload": {}, "processing_metadata": {}}\n'
    )
    report = check_silver("ds", "variables", path)
    assert report.passed

def test_silver_measurements_passes(tmp_path: Path) -> None:
    path = tmp_path / "measurements.jsonl"
    path.write_text(
        '{"dataset_id": "ds", "source": "src", "entity": "measurements", "natural_key": "k1", "attributes": {}, "source_payload": {}, "processing_metadata": {}}\n'
    )
    report = check_silver("ds", "measurements", path)
    assert report.passed

def test_silver_missing_file() -> None:
    report = check_silver("ds", "stations", Path("non-existent.jsonl"))
    assert not report.passed
    assert any("File not found" in r.message for r in report.results)

def test_silver_invalid_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "invalid.jsonl"
    path.write_text('{"valid": "json"}\n{invalid json}')
    report = check_silver("ds", "stations", path)
    assert not report.passed
    assert any("Failed to parse JSONL" in r.message for r in report.results)

def test_silver_empty_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "empty.jsonl"
    path.write_text("")
    report = check_silver("ds", "stations", path)
    assert not report.passed
    assert any("File has no records" in r.message for r in report.results)

def test_silver_missing_required_field(tmp_path: Path) -> None:
    path = tmp_path / "missing_field.jsonl"
    # Missing dataset_id
    path.write_text(
        '{"source": "src", "entity": "stations", "attributes": {}, "source_payload": {}, "processing_metadata": {}}\n'
    )
    report = check_silver("ds", "stations", path)
    assert not report.passed
    assert any("minimal_silver_structure" in r.check_name and not r.passed for r in report.results)

def test_silver_unsupported_entity(tmp_path: Path) -> None:
    path = tmp_path / "unsupported.jsonl"
    path.write_text('{"entity": "unknown"}\n')
    report = check_silver("ds", "unknown", path)
    assert not report.passed
    assert any("Unsupported entity" in r.message for r in report.results)

def test_silver_record_entity_mismatch(tmp_path: Path) -> None:
    path = tmp_path / "mismatch.jsonl"
    path.write_text(
        '{"dataset_id": "ds", "source": "src", "entity": "variables", "natural_key": "k1", "attributes": {}, "source_payload": {}, "processing_metadata": {}}\n'
    )
    report = check_silver("ds", "stations", path)
    assert not report.passed
    assert any("entity_match" in r.check_name and not r.passed for r in report.results)

def test_silver_natural_key_can_be_null(tmp_path: Path) -> None:
    path = tmp_path / "null_key.jsonl"
    path.write_text(
        '{"dataset_id": "ds", "source": "src", "entity": "stations", "natural_key": null, "attributes": {}, "source_payload": {}, "processing_metadata": {}}\n'
    )
    report = check_silver("ds", "stations", path)
    assert report.passed
