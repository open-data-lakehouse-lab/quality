
SUPPORTED_RESOURCES = [
    "stations-metadata",
    "variables-metadata",
    "measured-variable",
]

def validate_resource(resource: str) -> None:
    """Validate that the resource is supported."""
    if resource not in SUPPORTED_RESOURCES:
        raise ValueError(
            f"Unsupported resource: {resource}. Supported: {', '.join(SUPPORTED_RESOURCES)}"
        )
