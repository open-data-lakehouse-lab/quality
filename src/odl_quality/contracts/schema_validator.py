import json
from pathlib import Path
from typing import Any
import jsonschema  # type: ignore
from odl_quality.models.result import QualityCheckResult

class SchemaValidator:
    def validate(self, payload: Any, schema_path: Path) -> QualityCheckResult:
        """
        Validate payload against schema.
        """
        if not schema_path.exists():
            return QualityCheckResult(
                check_name="schema_validation",
                passed=False,
                message=f"Schema file not found: {schema_path}"
            )

        try:
            with open(schema_path, "r") as f:
                schema_data = json.load(f)
        except json.JSONDecodeError as e:
            return QualityCheckResult(
                check_name="schema_validation",
                passed=False,
                message=f"Invalid schema JSON at {schema_path}: {e}"
            )
        except Exception as e:
            return QualityCheckResult(
                check_name="schema_validation",
                passed=False,
                message=f"Failed to load schema: {e}"
            )

        try:
            jsonschema.validate(instance=payload, schema=schema_data)
            return QualityCheckResult(
                check_name="schema_validation",
                passed=True,
                message="Payload matches contract schema",
                details={"schema": str(schema_path)}
            )
        except jsonschema.exceptions.ValidationError as e:
            return QualityCheckResult(
                check_name="schema_validation",
                passed=False,
                message=f"Payload does not match schema: {e.message}",
                details={"schema": str(schema_path), "error": str(e)}
            )
        except jsonschema.exceptions.SchemaError as e:
            return QualityCheckResult(
                check_name="schema_validation",
                passed=False,
                message=f"Invalid schema structure: {e.message}",
                details={"schema": str(schema_path), "error": str(e)}
            )
        except Exception as e:
            return QualityCheckResult(
                check_name="schema_validation",
                passed=False,
                message=f"Unexpected error during validation: {e}"
            )
