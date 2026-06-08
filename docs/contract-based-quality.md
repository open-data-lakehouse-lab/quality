# Contract-based Quality

The `quality` repository supports optional contract-based validation for landing payloads using draft dataset contracts and JSON schemas.

## Overview

Contract-based validation is an opt-in feature that allows validating landing JSON payloads against internal lab contracts. These contracts and schemas are located in the sibling `datasets-catalog` repository.

Important notes:
- Contracts are internal lab contracts, not official upstream contracts.
- Schemas are permissive and draft.
- No network access or API keys are required.
- It uses the `jsonschema` library for validation.

## Usage

To enable contract-based validation, use the `--use-contract` flag and provide the path to the datasets catalog with `--catalog-path`.

```bash
odl-quality check landing \
  --dataset meteocat-weather \
  --resource stations-metadata \
  --input-path ./examples/landing/stations-metadata.json \
  --catalog-path ../datasets-catalog \
  --use-contract
```

## Supported Datasets and Resources

Currently, contract-based validation is supported for:

- **Dataset**: `meteocat-weather`
- **Resources**:
  - `stations-metadata`
  - `variables-metadata`
  - `measured-variable`

## Contract Discovery

Contracts are loaded from the following path within the catalog:
`<catalog-path>/datasets/weather/meteocat/contracts/<resource>.contract.json`

The schema path is resolved relative to the dataset base path in the catalog using the `schema_ref` field in the contract.

## Implementation Details

- **Contract Loader**: `src/odl_quality/contracts/catalog_contract_loader.py` responsible for loading and basic validation of the contract JSON.
- **Schema Validator**: `src/odl_quality/contracts/schema_validator.py` responsible for validating the JSON payload against the schema using `jsonschema`.
