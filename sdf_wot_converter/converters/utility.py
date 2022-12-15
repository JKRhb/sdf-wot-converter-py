from typing import Dict

from jsonschema import ValidationError


def initialize_object_field(model: Dict, field_name: str) -> Dict:
    if field_name not in model:
        model[field_name] = {}

    return model[field_name]


def initialize_list_field(
    model: Dict, field_name: str, raise_error_if_exists=False
) -> list:
    if field_name not in model:
        model[field_name] = []
    elif raise_error_if_exists:
        # TODO: Revisit once decision on sdfChoice and enum has been made
        raise ValidationError("sdfChoice and enum can't be used simultaneously.")

    return model[field_name]


def ensure_value_is_list(value):
    if isinstance(value, list):
        return value

    return [value]


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
    """Maps a field from a source definition to a target definition, applying a
    conversion function if given."""
    source_value = source_definition.get(source_key)

    if source_value is None:
        return

    if conversion_function is not None:
        source_value = conversion_function(source_value)

    if mapped_fields is not None:
        mapped_fields.append(source_key)

    target_definition[target_key] = source_value


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
