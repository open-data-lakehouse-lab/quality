# Landing Quality

Landing checks focus on preserving the raw source payloads while ensuring basic data integrity.

## Current Checks

- **File existence**: Verifies that the input file exists.
- **Valid JSON**: Ensures the file is a well-formed JSON document.
- **Payload not empty**: Checks that the parsed JSON is not empty.
- **Resource support**: Validates that the resource name is known.

## Future Work

- **Source schema validation**: Adding schema-level validation for specific resources as they land.
