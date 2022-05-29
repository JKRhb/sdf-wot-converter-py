from ..utility import map_common_field


def map_common_json_schema_fields(source_definition: dict, target_definition: dict):
    """Maps dataschema fields which are equal for both SDF and WoT.

    These definitions can simply be copied over, creating a deep copy for each field
    in the process.
    """
    map_jsonschema_type(source_definition, target_definition)
    map_unit(source_definition, target_definition)
    map_const(source_definition, target_definition)
    map_default(source_definition, target_definition)
    map_multiple_of(source_definition, target_definition)
    map_min_length(source_definition, target_definition)
    map_max_length(source_definition, target_definition)
    map_min_items(source_definition, target_definition)
    map_max_items(source_definition, target_definition)
    map_minimum(source_definition, target_definition)
    map_maximum(source_definition, target_definition)
    map_required(source_definition, target_definition)
    map_format(source_definition, target_definition)
    map_unique_items(source_definition, target_definition)
    map_pattern(source_definition, target_definition)
    map_exclusive_minimum(source_definition, target_definition)
    map_exclusive_maximum(source_definition, target_definition)


def map_exclusive_maximum(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "exclusiveMaximum")


def map_exclusive_minimum(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "exclusiveMinimum")


def map_pattern(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "pattern")


def map_unique_items(source_definition, target_definition):
    # TODO: Move somewhere else
    map_common_field(source_definition, target_definition, "uniqueItems")


def map_format(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "format")


def map_required(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "required")


def map_maximum(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "maximum")


def map_minimum(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "minimum")


def map_max_items(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "maxItems")


def map_min_items(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "minItems")


def map_max_length(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "maxLength")


def map_min_length(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "minLength")


def map_multiple_of(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "multipleOf")


def map_default(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "default")


def map_const(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "const")


def map_unit(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "unit")


def map_jsonschema_type(source_definition, target_definition):
    map_common_field(source_definition, target_definition, "type")
