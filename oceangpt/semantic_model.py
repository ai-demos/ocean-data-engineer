import json

from oceangpt.ocean_tables import ocean_tables, ocean_table_relationships


def get_ocean_semantic_model() -> str:
    """Returns the semantic model of the ocean data protocol as a string"""

    sematic_model = {
        "tables": [table.model_dump(exclude_none=True) for table in ocean_tables],
        "relationships": [
            relationship.model_dump(exclude_none=True) for relationship in ocean_table_relationships
        ],
    }
    return json.dumps(sematic_model, indent=4)
