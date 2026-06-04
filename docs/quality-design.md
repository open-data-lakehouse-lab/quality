# Quality Design

The `quality` repository implements a local-first, lightweight validation layer for the Open Data Lakehouse Lab.

## Local-first Quality Validation

Validation is designed to run locally without requiring network access, API keys, or heavy infrastructure. This ensures fast feedback loops and independence from external services.

## Quality Result Model

The core of the system is the `QualityCheckResult` and `QualityReport` models, which provide a standardized way to represent validation outcomes.

## CLI Workflow

The `odl-quality` CLI allows users to run checks for different stages of the data pipeline:
- `landing`: Basic JSON and file-level checks.
- `bronze`: JSONL format and minimal record structure validation.

## Future Integration

- **Orchestration**: Quality checks can be integrated into CI/CD pipelines or workflow orchestrators.
- **Richer Frameworks**: Future versions may evaluate and incorporate more comprehensive data quality frameworks.
