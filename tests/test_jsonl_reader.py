from pathlib import Path
import pytest
from odl_quality.readers.jsonl_reader import read_jsonl

def test_read_jsonl_valid(tmp_path: Path) -> None:
    p = tmp_path / "valid.jsonl"
    p.write_text('{"a": 1}\n{"b": 2}\n')
    
    records = read_jsonl(p)
    assert len(records) == 2
    assert records[0] == {"a": 1}
    assert records[1] == {"b": 2}

def test_read_jsonl_invalid(tmp_path: Path) -> None:
    p = tmp_path / "invalid.jsonl"
    p.write_text('{"a": 1}\n{invalid}\n')
    
    with pytest.raises(ValueError, match="Invalid JSON at line 2"):
        read_jsonl(p)
