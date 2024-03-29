from typing import List
from .utility import map_common_field


def map_common_json_schema_fields(
    source_definition: dict, target_definition: dict, mapped_fields: List[str]
):
    """Maps dataschema fields which are equal for both SDF and WoT.

    As the fields which are being mapped here have the same format, they can be
    mapped by by simply copying them from the source to the target definition.
    The definition's key is added to a list of mapped_fields in order to exclude
    it from mappings of additional properties.
    """

    map_jsonschema_type(source_definition, target_definition, mapped_fields)
    map_unit(source_definition, target_definition, mapped_fields)
    map_const(source_definition, target_definition, mapped_fields)
    map_default(source_definition, target_definition, mapped_fields)
    map_multiple_of(source_definition, target_definition, mapped_fields)
    map_min_length(source_definition, target_definition, mapped_fields)
    map_max_length(source_definition, target_definition, mapped_fields)
    map_min_items(source_definition, target_definition, mapped_fields)
    map_max_items(source_definition, target_definition, mapped_fields)
    map_minimum(source_definition, target_definition, mapped_fields)
    map_maximum(source_definition, target_definition, mapped_fields)
    map_exclusive_minimum(source_definition, target_definition, mapped_fields)
    map_exclusive_maximum(source_definition, target_definition, mapped_fields)
    map_required(source_definition, target_definition, mapped_fields)
    map_format(source_definition, target_definition, mapped_fields)
    map_pattern(source_definition, target_definition, mapped_fields)


def map_pattern(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "pattern", mapped_fields=mapped_fields
    )


def map_format(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "format", mapped_fields=mapped_fields
    )


def map_required(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "required", mapped_fields=mapped_fields
    )


def map_maximum(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "maximum", mapped_fields=mapped_fields
    )


def map_minimum(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "minimum", mapped_fields=mapped_fields
    )


def map_exclusive_maximum(
    source_definition, target_definition, mapped_fields: List[str]
):
    map_common_field(
        source_definition,
        target_definition,
        "exclusiveMaximum",
        mapped_fields=mapped_fields,
    )


def map_exclusive_minimum(
    source_definition, target_definition, mapped_fields: List[str]
):
    map_common_field(
        source_definition,
        target_definition,
        "exclusiveMinimum",
        mapped_fields=mapped_fields,
    )


def map_max_items(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "maxItems", mapped_fields=mapped_fields
    )


def map_min_items(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "minItems", mapped_fields=mapped_fields
    )


def map_max_length(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "maxLength", mapped_fields=mapped_fields
    )


def map_min_length(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "minLength", mapped_fields=mapped_fields
    )


def map_multiple_of(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "multipleOf", mapped_fields=mapped_fields
    )


def map_default(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "default", mapped_fields=mapped_fields
    )


def map_const(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "const", mapped_fields=mapped_fields
    )


def map_unit(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "unit", mapped_fields=mapped_fields
    )


def map_jsonschema_type(source_definition, target_definition, mapped_fields: List[str]):
    map_common_field(
        source_definition, target_definition, "type", mapped_fields=mapped_fields
    )
