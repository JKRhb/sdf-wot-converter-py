import copy
from typing import Dict


def initialize_object_field(model: Dict, field_name: str):
    if field_name not in model:
        model[field_name] = {}


def initialize_list_field(model: Dict, field_name: str):
    if field_name not in model:
        model[field_name] = []


def negate(value: bool):
    """Negates a boolean value. Supposed to be used as a dedicated conversion
    function for `map_field` and `map_common_field` functions."""
    return not value


def map_field(
    source_definition: Dict,
    target_definition: Dict,
    source_key: str,
    target_key: str,
    conversion_function=None,
    mapped_fields=None,
):
    """Maps a field from a source defiinition to a target definition, making a deep
    copy in the process."""
    if source_key not in source_definition:
        return

    value = copy.deepcopy(source_definition[source_key])

    if conversion_function is not None:
        value = conversion_function(value)

    if mapped_fields is not None:
        mapped_fields.append(source_key)

    target_definition[target_key] = value


def map_common_field(
    source_definition: dict,
    target_definition: dict,
    common_key: str,
    conversion_function=None,
    mapped_fields=None,
):
    """Maps a field from a source defiinition to a target definition that has the same
    name in both definitions."""
    map_field(
        source_definition,
        target_definition,
        common_key,
        common_key,
        conversion_function=conversion_function,
        mapped_fields=mapped_fields,
    )
