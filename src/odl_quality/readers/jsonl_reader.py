import json
from pathlib import Path
from typing import Any, List

def read_jsonl(path: Path) -> List[Any]:
    """Read a local JSONL file."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at line {i} in {path}: {e}")
    
    return records
