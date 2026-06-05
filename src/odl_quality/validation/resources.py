
SUPPORTED_RESOURCES = [
    "stations-metadata",
    "variables-metadata",
    "measured-variable",
]

SUPPORTED_ENTITIES = [
    "stations",
    "variables",
    "measurements",
]

def validate_resource(resource: str) -> None:
    """Validate that the resource is supported."""
    if resource not in SUPPORTED_RESOURCES:
        raise ValueError(
            f"Unsupported resource: {resource}. Supported: {', '.join(SUPPORTED_RESOURCES)}"
        )

def validate_entity(entity: str) -> None:
    """Validate that the entity is supported."""
    if entity not in SUPPORTED_ENTITIES:
        raise ValueError(
            f"Unsupported entity: {entity}. Supported: {', '.join(SUPPORTED_ENTITIES)}"
        )
