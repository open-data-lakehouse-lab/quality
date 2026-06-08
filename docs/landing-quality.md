# Landing Quality

Landing checks focus on preserving the raw source payloads while ensuring basic data integrity.

## Current Checks

- **File existence**: Verifies that the input file exists.
- **Valid JSON**: Ensures the file is a well-formed JSON document.
- **Payload not empty**: Checks that the parsed JSON is not empty.
- **Resource support**: Validates that the resource name is known.
- **Contract-based validation (Optional)**: Validates the payload against a draft contract and JSON schema. See [Contract-based Quality](contract-based-quality.md) for more details.

## Future Work

- **Enhanced schema validation**: Adding more strict validation rules.
