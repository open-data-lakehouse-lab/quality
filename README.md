# Open Data Lakehouse Lab - Quality

The `quality` repository is responsible for local data quality validation in the Open Data Lakehouse Lab project.

## Purpose

This repository provides lightweight, local-first quality checks for:
- Landing JSON files.
- Bronze JSONL files.
- Minimal bronze record structure.

## Current Scope

- **Landing quality**: Verify file existence, valid JSON format, and non-empty payloads.
- **Bronze quality**: Verify file existence, valid JSONL format, and presence of mandatory bronze fields.
- **Meteocat resources**: Support for `stations-metadata`, `variables-metadata`, and `measured-variable`.

Checks are intentionally minimal and local-first. They do not require network access or API keys.

## Getting Started

### Install dependencies

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pip install -e .
```

### Run the CLI

```bash
odl-quality version

# Check landing data
odl-quality check landing \
  --dataset meteocat-weather \
  --resource stations-metadata \
  --input-path ./examples/landing/stations-metadata.json

# Check bronze data
odl-quality check bronze \
  --dataset meteocat-weather \
  --resource stations-metadata \
  --input-path ./examples/bronze/stations-metadata.jsonl
```

### Run validation

To run linting and tests:

```bash
bash scripts/validate.sh
```

## License

Unless otherwise noted:

- Software, scripts, Infrastructure as Code, SQL models, configuration files and executable assets are licensed under the [Apache License 2.0](LICENSE).
- Documentation, diagrams and written content are licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

Original upstream datasets, when referenced, remain governed by their original source licenses and terms.
