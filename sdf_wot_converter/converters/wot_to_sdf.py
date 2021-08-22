from typing import (
    Any,
    Dict,
)
from .utility import (
    initialize_list_field,
    initialize_object_field,
)
from jsonpointer import set_pointer
from . import wot_common


def initialize_object_from_json_pointer(sdf_model: Dict, json_pointer: str):
    current_element = sdf_model
    for element in json_pointer.split("/"):
        if not element or element == "#":
            continue  # pragma: no cover
        initialize_object_field(current_element, element)
        current_element = current_element[element]


def determine_json_pointer(sdf_model, base_field_name, key, property):
    json_pointer = f"/{base_field_name}/{key}"
    if "sdf:jsonPointer" in property:
        json_pointer = property["sdf:jsonPointer"][1:]
    initialize_object_from_json_pointer(sdf_model, json_pointer)
    return json_pointer


def map_properties(thing_model: Dict, sdf_model: Dict):
    for key, wot_property in thing_model.get("properties", {}).items():
        json_pointer = determine_json_pointer(
            sdf_model, "sdfProperty", key, wot_property
        )
        sdf_property: Dict[str, Any] = {}
        map_interaction_affordance_fields(wot_property, sdf_property)
        map_data_schema_fields(wot_property, sdf_property)

        set_pointer(sdf_model, json_pointer, sdf_property)


def map_items(wot_definition: Dict, sdf_definition: Dict):
    if "items" in wot_definition:
        sdf_definition["items"] = {}
        map_data_schema_fields(wot_definition["items"], sdf_definition["items"])


def map_dataschema_properties(wot_definition: Dict, sdf_definition: Dict):
    for key, property in wot_definition.get("properties", {}).items():
        initialize_object_field(sdf_definition, "properties")
        sdf_definition["properties"][key] = {}
        map_data_schema_fields(property, sdf_definition["properties"][key])


def map_actions(thing_model: Dict, sdf_model: Dict):
    for key, wot_action in thing_model.get("actions", {}).items():
        json_pointer = determine_json_pointer(sdf_model, "sdfAction", key, wot_action)
        sdf_action: Dict[str, Any] = {}
        map_sdf_comment(wot_action, sdf_action)
        map_interaction_affordance_fields(wot_action, sdf_action)
        map_action_fields(wot_action, sdf_action)
        set_pointer(sdf_model, json_pointer, sdf_action)


def map_action_fields(wot_action, sdf_action):
    # TODO: Missing fields: safe, idempotent
    if "input" in wot_action:
        sdf_input_data = {}
        map_data_schema_fields(wot_action["input"], sdf_input_data)
        sdf_action["sdfInputData"] = sdf_input_data
    if "output" in wot_action:
        sdf_output_data = {}
        map_data_schema_fields(wot_action["output"], sdf_output_data)
        sdf_action["sdfOutputData"] = sdf_output_data


def map_events(thing_model: Dict, sdf_model: Dict):
    for key, wot_event in thing_model.get("events", {}).items():
        json_pointer = determine_json_pointer(sdf_model, "sdfEvent", key, wot_event)
        sdf_event: Dict[str, Any] = {}
        map_sdf_comment(wot_event, sdf_event)
        map_interaction_affordance_fields(wot_event, sdf_event)
        map_event_fields(wot_event, sdf_event)
        set_pointer(sdf_model, json_pointer, sdf_event)


def map_event_fields(wot_event, sdf_event):
    # TODO: Missing fields: subscription, cancellation
    if "data" in wot_event:
        sdf_input_data = {}
        map_data_schema_fields(wot_event["data"], sdf_input_data)
        sdf_event["sdfOutputData"] = sdf_input_data


def map_data_schema_fields(wot_definition: Dict, sdf_definition: Dict):
    # TODO: Unmapped fields: @type, titles, descriptions, oneOf,
    # TODO: Deal with sdfType and nullable
    map_sdf_comment(wot_definition, sdf_definition)

    map_title(wot_definition, sdf_definition)
    map_description(wot_definition, sdf_definition)
    map_const(wot_definition, sdf_definition)
    map_default(wot_definition, sdf_definition)
    map_unit(wot_definition, sdf_definition)
    map_enum(wot_definition, sdf_definition)
    map_read_only(wot_definition, sdf_definition)
    map_write_only(wot_definition, sdf_definition)
    map_format(wot_definition, sdf_definition)
    map_jsonschema_type(wot_definition, sdf_definition)
    map_observable(wot_definition, sdf_definition)

    map_multiple_of(wot_definition, sdf_definition)
    map_min_length(wot_definition, sdf_definition)
    map_max_length(wot_definition, sdf_definition)
    map_min_items(wot_definition, sdf_definition)
    map_max_items(wot_definition, sdf_definition)
    map_minimum(wot_definition, sdf_definition)
    map_maximum(wot_definition, sdf_definition)
    map_required(wot_definition, sdf_definition)
    map_unique_items(wot_definition, sdf_definition)
    map_pattern(wot_definition, sdf_definition)
    map_exclusive_minimum(wot_definition, sdf_definition)
    map_exclusive_maximum(wot_definition, sdf_definition)
    map_content_format(wot_definition, sdf_definition)

    map_items(wot_definition, sdf_definition)
    map_dataschema_properties(wot_definition, sdf_definition)


def map_const(wot_definition: Dict, sdf_definition: Dict):
    if "const" in wot_definition:
        sdf_definition["const"] = wot_definition["const"]


def map_multiple_of(wot_definition: Dict, sdf_definition: Dict):
    if "multipleOf" in wot_definition:
        sdf_definition["multipleOf"] = wot_definition["multipleOf"]


def map_min_length(wot_definition: Dict, sdf_definition: Dict):
    if "minLength" in wot_definition:
        sdf_definition["minLength"] = wot_definition["minLength"]


def map_max_length(wot_definition: Dict, sdf_definition: Dict):
    if "maxLength" in wot_definition:
        sdf_definition["maxLength"] = wot_definition["maxLength"]


def map_min_items(wot_definition: Dict, sdf_definition: Dict):
    if "minItems" in wot_definition:
        sdf_definition["minItems"] = wot_definition["minItems"]


def map_max_items(wot_definition: Dict, sdf_definition: Dict):
    if "maxItems" in wot_definition:
        sdf_definition["maxItems"] = wot_definition["maxItems"]


def map_minimum(wot_definition: Dict, sdf_definition: Dict):
    if "minimum" in wot_definition:
        sdf_definition["minimum"] = wot_definition["minimum"]


def map_maximum(wot_definition: Dict, sdf_definition: Dict):
    if "maximum" in wot_definition:
        sdf_definition["maximum"] = wot_definition["maximum"]


def map_required(wot_definition: Dict, sdf_definition: Dict):
    if "required" in wot_definition:
        sdf_definition["required"] = wot_definition["required"]


def map_unique_items(wot_definition: Dict, sdf_definition: Dict):
    if "uniqueItems" in wot_definition:
        sdf_definition["uniqueItems"] = wot_definition["uniqueItems"]


def map_pattern(wot_definition: Dict, sdf_definition: Dict):
    if "pattern" in wot_definition:
        sdf_definition["pattern"] = wot_definition["pattern"]


def map_exclusive_minimum(wot_definition: Dict, sdf_definition: Dict):
    if "exclusiveMinimum" in wot_definition:
        sdf_definition["exclusiveMinimum"] = wot_definition["exclusiveMinimum"]


def map_exclusive_maximum(wot_definition: Dict, sdf_definition: Dict):
    if "exclusiveMaximum" in wot_definition:
        sdf_definition["exclusiveMaximum"] = wot_definition["exclusiveMaximum"]


def map_content_format(wot_definition: Dict, sdf_definition: Dict):
    if "contentMediaType" in wot_definition:
        sdf_definition["contentFormat"] = wot_definition["contentMediaType"]


def map_default(wot_definition: Dict, sdf_definition: Dict):
    if "default" in wot_definition:
        sdf_definition["default"] = wot_definition["default"]


def map_unit(wot_definition: Dict, sdf_definition: Dict):
    if "unit" in wot_definition:
        sdf_definition["unit"] = wot_definition["unit"]


def map_enum(wot_definition: Dict, sdf_definition: Dict):
    # TODO: Map enum to sdfChoice
    if "enum" in wot_definition:
        sdf_definition["enum"] = wot_definition["enum"]


def map_read_only(wot_definition: Dict, sdf_definition: Dict):
    if "readOnly" in wot_definition:
        sdf_definition["writable"] = not wot_definition["readOnly"]


def map_write_only(wot_definition: Dict, sdf_definition: Dict):
    if "writeOnly" in wot_definition:
        sdf_definition["readable"] = not wot_definition["writeOnly"]


def map_format(wot_definition: Dict, sdf_definition: Dict):
    if "format" in wot_definition:
        sdf_definition["format"] = wot_definition["format"]


def map_jsonschema_type(wot_definition: Dict, sdf_definition: Dict):
    # TODO: How to deal with NULL type?
    if "type" in wot_definition:
        sdf_definition["type"] = wot_definition["type"]


def map_observable(wot_definition: Dict, sdf_definition: Dict):
    if "observable" in wot_definition:
        sdf_definition["observable"] = wot_definition["observable"]
    elif "sdf:observable" in wot_definition:
        sdf_definition["observable"] = wot_definition["sdf:observable"]


def map_interaction_affordance_fields(wot_definition: Dict, sdf_definition: Dict):
    # TODO: Unmapped fields: @type, titles, descriptions, forms, uriVariables
    map_title(wot_definition, sdf_definition)
    map_description(wot_definition, sdf_definition)


def map_title(wot_definition: Dict, sdf_definition: Dict):
    if "title" in wot_definition:
        sdf_definition["label"] = wot_definition["title"]


def map_description(wot_definition: Dict, sdf_definition: Dict):
    if "description" in wot_definition:
        sdf_definition["description"] = wot_definition["description"]


def map_schema_definitions(thing_model: Dict, sdf_model: Dict):
    for key, wot_schema_definitions in thing_model.get("schemaDefinitions", {}).items():
        json_pointer = determine_json_pointer(
            sdf_model, "sdfData", key, wot_schema_definitions
        )
        sdf_data: Dict[str, Any] = {}
        map_sdf_comment(wot_schema_definitions, sdf_data)
        map_data_schema_fields(wot_schema_definitions, sdf_data)
        set_pointer(sdf_model, json_pointer, sdf_data)


def initialize_empty_string_field(sdf_definition: Dict, field_name: str):
    if field_name not in sdf_definition:
        sdf_definition[field_name] = ""


def initialize_info_block(sdf_model: Dict):
    initialize_object_field(sdf_model, "info")
    infoblock = sdf_model["info"]

    for field in ["title", "copyright", "version", "license"]:
        initialize_empty_string_field(infoblock, field)


def map_thing_title(wot_definition: Dict, sdf_definition: Dict):
    if "title" in wot_definition:
        initialize_info_block(sdf_definition)
        sdf_definition["info"]["title"] = wot_definition["title"]


def map_thing_description(wot_definition: Dict, sdf_definition: Dict):
    if "description" in wot_definition:
        initialize_info_block(sdf_definition)
        sdf_definition["info"]["copyright"] = wot_definition["description"]


def map_links(wot_definition: Dict, sdf_definition: Dict):
    # TODO: Deal with other link types
    for link in wot_definition.get("links", []):
        if link.get("rel") == "license":
            initialize_info_block(sdf_definition)
            sdf_definition["info"]["license"] = link["href"]


def map_version(wot_definition: Dict, sdf_definition: Dict):
    version_info = wot_definition.get("version", {})
    if "model" in version_info:
        initialize_info_block(sdf_definition)
        sdf_definition["info"]["version"] = version_info["model"]


def map_context(wot_definition: Dict, sdf_definition: Dict):
    # TODO: How to deal with context elements without namespace?
    context = wot_definition["@context"]
    if isinstance(context, str):
        pass
    else:
        for context_element in context:
            if isinstance(context_element, dict):
                for namespace, url in context_element.items():
                    if namespace == "sdf":
                        continue
                    else:
                        initialize_object_field(sdf_definition, "namespace")
                        sdf_definition["namespace"][namespace] = url
            else:
                continue  # pragma: no cover

    if "sdf:defaultNamespace" in wot_definition:
        sdf_definition["defaultNamespace"] = wot_definition["sdf:defaultNamespace"]


def map_sdf_comment(wot_definition: Dict, sdf_definition: Dict):
    # TODO: Move somewhere else
    if "sdf:$comment" in wot_definition:
        sdf_definition["$comment"] = wot_definition["sdf:$comment"]


def convert_wot_tm_to_sdf(thing_model: Dict, placeholder_map=None) -> Dict:
    # TODO: Unmapped fields: @type, id, titles, descriptions, created,
    #       modified, support, base, forms, security,
    #       securityDefinitions, profile, schemaDefinitions
    sdf_model: Dict = {}

    thing_model = wot_common.resolve_extension(thing_model)
    thing_model = wot_common.replace_placeholders(thing_model, placeholder_map)

    map_thing_title(thing_model, sdf_model)
    map_thing_description(thing_model, sdf_model)
    map_links(thing_model, sdf_model)
    map_version(thing_model, sdf_model)
    map_context(thing_model, sdf_model)

    map_properties(thing_model, sdf_model)
    map_actions(thing_model, sdf_model)
    map_events(thing_model, sdf_model)
    map_schema_definitions(thing_model, sdf_model)

    return sdf_model
