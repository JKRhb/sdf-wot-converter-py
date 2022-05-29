import copy
from typing import Dict
from ..schemas.sdf_validation_schema import sdf_validation_schema
from ..schemas.td_schema import td_schema
from ..schemas.tm_schema import tm_schema
from jsonschema import Draft7Validator


def initialize_object_field(model: Dict, field_name: str):
    if field_name not in model:
        model[field_name] = {}


def initialize_list_field(model: Dict, field_name: str):
    if field_name not in model:
        model[field_name] = []


def validate_sdf_model(sdf_model: Dict):
    Draft7Validator(sdf_validation_schema).validate(sdf_model)


def validate_thing_model(thing_model: Dict):
    Draft7Validator(tm_schema).validate(thing_model)


def validate_thing_description(thing_description: Dict):
    Draft7Validator(td_schema).validate(thing_description)


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
):
    """Maps a field from a source defiinition to a target definition, making a deep
    copy in the process."""
    if source_key not in source_definition:
        return

    value = copy.deepcopy(source_definition[source_key])

    if conversion_function is not None:
        value = conversion_function(value)

    target_definition[target_key] = value


def map_common_field(
    source_definition: dict,
    target_definition: dict,
    common_key: str,
    conversion_function=None,
):
    """Maps a field from a source defiinition to a target definition that has the same
    name in both definitions."""
    map_field(
        source_definition,
        target_definition,
        common_key,
        common_key,
        conversion_function=conversion_function,
    )
