# Bronze Quality

Bronze checks ensure that the data transformed into JSONL format adheres to the minimal required structure for the bronze layer.

## Required Fields

Every bronze record must contain:
- `dataset_id`
- `source`
- `resource`
- `record_type`
- `payload`
- `processing_metadata`

## Current Checks

- **Valid JSONL**: Ensures the file is a well-formed JSON Lines document.
- **Record presence**: Verifies that the file contains at least one record.
- **Minimal structure**: Validates the presence of mandatory bronze fields in every record.

## Future Work

- **Silver/Gold quality rules**: Business-level validation and schema enforcement will be added in later stages.
