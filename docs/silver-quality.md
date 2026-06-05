# Silver Quality

Silver checks ensure that the data transformed into the Silver foundation adheres to the minimal required structure for the Silver layer.

## Required Fields

Every Silver record must contain:

- `dataset_id`
- `source`
- `entity`
- `attributes`
- `source_payload`
- `processing_metadata`

The following field is optional and can be `null`:

- `natural_key`

## Supported Entities

The current Silver layer supports:

- `stations`
- `variables`
- `measurements`

## Current Checks

- **File existence**: Verifies that the input path exists.
- **Valid JSONL**: Ensures the file is a well-formed JSON Lines document.
- **Record presence**: Verifies that the file contains at least one record.
- **Minimal structure**: Validates the presence of mandatory Silver fields in every record.
- **Entity support**: Ensures the requested `--entity` is supported by the platform.
- **Entity consistency**: Validates that every record in the file has an `entity` field that matches the expected `--entity`.

## Usage

```bash
odl-quality check silver \
  --dataset meteocat-weather \
  --entity stations \
  --input-path ./examples/silver/stations.jsonl
```

## Note on Quality Frameworks

At this stage, Silver checks are still minimal and focused on technical integrity. No external data quality framework is used at this stage, keeping the project lightweight, local-first, independent, and neutral.

## Related documentation

- [Bronze Quality](bronze-quality.md)
- [Quality Design](quality-design.md)
