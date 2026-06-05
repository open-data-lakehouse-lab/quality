from typing import Any, List, Optional
from pydantic import BaseModel

class QualityCheckResult(BaseModel):
    check_name: str
    passed: bool
    message: str
    details: Optional[Any] = None

class QualityReport(BaseModel):
    dataset: str
    resource: str  # This represents either resource (bronze) or entity (silver)
    results: List[QualityCheckResult]
    
    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)
