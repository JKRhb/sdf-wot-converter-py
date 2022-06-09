import copy
import os
from typing import (
    Any,
    Dict,
    List,
    Set,
    Tuple,
    Union,
)

from .common.jsonschema import (
    map_common_json_schema_fields,
)
from ..validation import validate_sdf_model
from .utility import (
    initialize_list_field,
    initialize_object_field,
    map_field,
    map_common_field,
    negate,
)
from .wot_common import (
    is_thing_collection,
    replace_placeholders,
    resolve_extension,
    retrieve_thing_model,
)
import urllib.parse


def map_properties(
    thing_model: Dict,
    sdf_model: Dict,
    sdf_mapping_file,
    current_path: str,
    mapped_fields: List[str],
):
    if "properties" not in thing_model:
        return

    mapped_fields.append("properties")

    for key, wot_property in thing_model["properties"].items():
        initialize_object_field(sdf_model, "sdfProperty")
        sdf_property: Dict[str, Any] = {}
        mapped_property_fields: List[str] = []
        property_path = f"{current_path}/sdfProperty/{key}"

        map_interaction_affordance_fields(
            wot_property, sdf_property, mapped_property_fields
        )
        map_observable(wot_property, sdf_property, mapped_property_fields)
        map_data_schema_fields(
            thing_model,
            wot_property,
            sdf_property,
            sdf_mapping_file,
            current_path,
            is_property=True,
            mapped_fields=mapped_property_fields,
            property_path=property_path,
        )

        sdf_model["sdfProperty"][key] = sdf_property


def map_items(
    thing_model,
    wot_definition: Dict,
    sdf_definition: Dict,
    sdf_mapping_file: Dict,
    current_path: str,
    mapped_fields: List[str],
):
    if "items" in wot_definition:
        mapped_fields.append("items")
        sdf_definition["items"] = {}
        map_data_schema_fields(
            thing_model,
            wot_definition["items"],
            sdf_definition["items"],
            sdf_mapping_file,
            current_path,
        )


def map_dataschema_properties(
    thing_model,
    wot_definition: Dict,
    sdf_definition: Dict,
    sdf_mapping_file: Dict,
    current_path: str,
    mapped_fields: List[str],
):
    if "properties" not in wot_definition:
        return

    mapped_fields.append("properties")

    for key, property in wot_definition["properties"].items():
        initialize_object_field(sdf_definition, "properties")
        sdf_definition["properties"][key] = {}
        map_data_schema_fields(
            thing_model,
            property,
            sdf_definition["properties"][key],
            sdf_mapping_file,
            current_path,
        )


def map_actions(
    thing_model: Dict,
    sdf_model: Dict,
    sdf_mapping_file,
    current_path: str,
    mapped_fields: List[str],
):
    if "actions" not in thing_model:
        return

    mapped_fields.append("actions")

    for key, wot_action in thing_model["actions"].items():
        initialize_object_field(sdf_model, "sdfAction")
        sdf_action: Dict[str, Any] = {}
        mapped_action_fields: List[str] = []
        action_path = f"{current_path}/sdfAction/{key}"

        map_sdf_comment(wot_action, sdf_action, mapped_action_fields)
        map_interaction_affordance_fields(wot_action, sdf_action, mapped_action_fields)
        map_action_fields(
            thing_model,
            wot_action,
            sdf_action,
            sdf_mapping_file,
            current_path,
            mapped_action_fields,
        )
        map_tm_ref(
            thing_model, wot_action, sdf_action, current_path, mapped_action_fields
        )

        map_additional_fields(
            sdf_mapping_file, wot_action, action_path, mapped_action_fields
        )

        sdf_model["sdfAction"][key] = sdf_action


def map_action_fields(
    thing_model,
    wot_action,
    sdf_action,
    sdf_mapping_file,
    current_path: str,
    mapped_fields: List[str],
):
    # TODO: Missing fields: safe, idempotent
    if "input" in wot_action:
        sdf_input_data: Dict[str, Any] = {}
        mapped_fields.append("input")
        map_data_schema_fields(
            thing_model,
            wot_action["input"],
            sdf_input_data,
            sdf_mapping_file,
            current_path,
        )
        sdf_action["sdfInputData"] = sdf_input_data
    if "output" in wot_action:
        sdf_output_data: Dict[str, Any] = {}
        mapped_fields.append("output")
        map_data_schema_fields(
            thing_model,
            wot_action["output"],
            sdf_output_data,
            sdf_mapping_file,
            current_path,
        )
        sdf_action["sdfOutputData"] = sdf_output_data


def map_events(
    thing_model: Dict,
    sdf_model: Dict,
    sdf_mapping_file,
    current_path: str,
    mapped_fields: List[str],
):
    if "events" not in thing_model:
        return

    mapped_fields.append("events")

    for key, wot_event in thing_model["events"].items():
        initialize_object_field(sdf_model, "sdfEvent")
        sdf_event: Dict[str, Any] = {}
        mapped_event_fields: List[str] = []
        event_path = f"{current_path}/sdfEvent/{key}"

        map_sdf_comment(wot_event, sdf_event, mapped_event_fields)
        map_interaction_affordance_fields(wot_event, sdf_event, mapped_event_fields)
        map_event_fields(
            thing_model,
            wot_event,
            sdf_event,
            sdf_mapping_file,
            current_path,
            mapped_event_fields,
        )
        map_tm_ref(thing_model, wot_event, sdf_event, current_path, mapped_event_fields)

        map_additional_fields(
            sdf_mapping_file, wot_event, event_path, mapped_event_fields
        )

        sdf_model["sdfEvent"][key] = sdf_event


def map_event_fields(
    thing_model,
    wot_event,
    sdf_event,
    sdf_mapping_file: Dict,
    current_path: str,
    mapped_fields: List[str],
):
    # TODO: Missing fields: subscription, cancellation
    if "data" in wot_event:
        sdf_input_data: Dict = {}
        mapped_fields.append("data")
        map_data_schema_fields(
            thing_model,
            wot_event["data"],
            sdf_input_data,
            sdf_mapping_file,
            current_path,
            mapped_fields,
        )
        sdf_event["sdfOutputData"] = sdf_input_data


def map_data_schema_fields(
    thing_model,
    wot_definition: Dict,
    sdf_definition: Dict,
    sdf_mapping_file: Dict,
    current_path: str,
    is_property=False,
    mapped_fields=None,
    property_path=None,
):
    if mapped_fields is None:
        mapped_fields = []

    mapping_file_path = current_path
    if property_path is not None:
        mapping_file_path = property_path

    map_sdf_comment(wot_definition, sdf_definition, mapped_fields)

    map_common_json_schema_fields(wot_definition, sdf_definition, mapped_fields)

    map_title(wot_definition, sdf_definition, mapped_fields)
    map_description(wot_definition, sdf_definition, mapped_fields)
    map_enum(wot_definition, sdf_definition, mapped_fields)
    if is_property:
        # TODO: Add mapping for when not part of dataschema
        map_read_only(wot_definition, sdf_definition, mapped_fields)
        map_write_only(wot_definition, sdf_definition, mapped_fields)
    map_unique_items(wot_definition, sdf_definition, mapped_fields)
    map_content_format(wot_definition, sdf_definition, mapped_fields)
    map_nullable(wot_definition, sdf_definition, mapped_fields)
    map_sdf_type(wot_definition, sdf_definition, mapped_fields)

    map_items(
        thing_model,
        wot_definition,
        sdf_definition,
        sdf_mapping_file,
        current_path,
        mapped_fields,
    )
    map_dataschema_properties(
        thing_model,
        wot_definition,
        sdf_definition,
        sdf_mapping_file,
        current_path,
        mapped_fields,
    )

    map_tm_ref(thing_model, wot_definition, sdf_definition, current_path, mapped_fields)

    map_additional_fields(
        sdf_mapping_file, wot_definition, mapping_file_path, mapped_fields
    )


def map_nullable(wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]):
    map_field(
        wot_definition,
        sdf_definition,
        "sdf:nullable",
        "nullable",
        mapped_fields=mapped_fields,
    )


def map_sdf_type(wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]):
    map_field(
        wot_definition,
        sdf_definition,
        "sdf:sdfType",
        "sdfType",
        mapped_fields=mapped_fields,
    )


def map_unique_items(
    wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]
):
    map_common_field(
        wot_definition, sdf_definition, "uniqueItems", mapped_fields=mapped_fields
    )


def map_content_format(
    wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]
):
    map_field(
        wot_definition,
        sdf_definition,
        "contentMediaType",
        "contentFormat",
        mapped_fields=mapped_fields,
    )


def map_enum(wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]):
    if "enum" in wot_definition:
        mapped_fields.append("enum")
        for enum in wot_definition["enum"]:
            if type(enum) is dict and "sdf:choiceName" in enum:
                initialize_object_field(sdf_definition, "sdfChoice")
                choice_name = enum["sdf:choiceName"]
                sdf_definition["sdfChoice"][choice_name] = enum
                del sdf_definition["sdfChoice"][choice_name]["sdf:choiceName"]
            else:
                initialize_list_field(sdf_definition, "enum")
                sdf_definition["enum"].append(enum)


def map_read_only(wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]):
    map_field(
        wot_definition,
        sdf_definition,
        "readOnly",
        "writable",
        conversion_function=negate,
        mapped_fields=mapped_fields,
    )


def map_write_only(
    wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]
):
    map_field(
        wot_definition,
        sdf_definition,
        "writeOnly",
        "readable",
        conversion_function=negate,
        mapped_fields=mapped_fields,
    )


def map_observable(wot_property: Dict, sdf_property: Dict, mapped_fields: List[str]):
    mapped_fields.append("observable")
    sdf_property["observable"] = wot_property.get("observable", False)


def map_interaction_affordance_fields(
    wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]
):
    # TODO: Unmapped fields: @type, titles, descriptions, forms, uriVariables
    map_title(wot_definition, sdf_definition, mapped_fields)
    map_description(wot_definition, sdf_definition, mapped_fields)


def map_title(wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]):
    map_field(
        wot_definition, sdf_definition, "title", "label", mapped_fields=mapped_fields
    )


def map_description(
    wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]
):
    map_common_field(
        wot_definition, sdf_definition, "description", mapped_fields=mapped_fields
    )


def map_schema_definitions(
    thing_model: Dict,
    sdf_model: Dict,
    sdf_mapping_file,
    current_path: str,
    mapped_fields: List[str],
):
    if "schemaDefinitions" not in thing_model:
        return

    mapped_fields.append("schemaDefinitions")

    for key, wot_schema_definitions in thing_model["schemaDefinitions"].items():
        if "sdfData" not in sdf_model:
            sdf_model["sdfData"] = {}
        sdf_data: Dict[str, Any] = {}
        mapped_schema_definitions_fields: List[str] = []
        map_sdf_comment(
            wot_schema_definitions, sdf_data, mapped_schema_definitions_fields
        )
        map_data_schema_fields(
            thing_model,
            wot_schema_definitions,
            sdf_data,
            sdf_mapping_file,
            current_path,
            mapped_fields=mapped_schema_definitions_fields,
        )
        map_tm_ref(
            thing_model,
            wot_schema_definitions,
            sdf_data,
            current_path,
            mapped_schema_definitions_fields,
        )

        sdf_model["sdfData"][key] = sdf_data


def map_links(
    wot_definition: Dict,
    sdf_definition: Dict,
    sdf_mapping_file,
    mapped_fields: List[str],
):
    if "links" not in wot_definition:
        return

    mapped_fields.append("links")

    # TODO: Deal with other link types
    for link in wot_definition["links"]:
        if link.get("rel") == "license":
            continue


def map_version(
    wot_definition: Dict,
    sdf_definition: Dict,
    sdf_mapping_file: Dict,
    mapped_fields: List[str],
):
    if "version" not in wot_definition:
        return

    mapped_fields.append("version")

    version_info = wot_definition["version"]
    if "model" in version_info:
        for sdf_dict in [sdf_definition, sdf_mapping_file]:
            pass
            # initialize_info_block(sdf_dict)
            # sdf_dict["info"]["version"] = version_info["model"]


def map_context(wot_definition: Dict, sdf_definition: Dict, sdf_mapping_file):
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


def map_sdf_comment(
    wot_definition: Dict, sdf_definition: Dict, mapped_fields: List[str]
):
    map_field(
        wot_definition,
        sdf_definition,
        "sdf:$comment",
        "$comment",
        mapped_fields=mapped_fields,
    )


def convert_pointer(pointer: str, current_path: str) -> str:
    # TODO: Maybe this can be done more elegantly
    # TODO: Check if there are more possible mappings
    pointer = pointer.replace("events", "sdfEvent")
    pointer = pointer.replace("actions", "sdfAction")
    pointer = pointer.replace("properties", "sdfProperty")
    pointer = pointer.replace("schemaDefinitions", "sdfData")
    pointer = pointer.replace("input", "sdfInputData")
    pointer = pointer.replace("output", "sdfOutputData")
    return current_path + pointer[1:]


def map_tm_ref(
    wot_model: Dict,
    wot_definition: Dict,
    sdf_definition: Dict,
    current_path: str,
    mapped_fields: List[str],
):
    if "tm:ref" in wot_definition:
        pointer = wot_definition["tm:ref"]
        mapped_fields.append("tm:ref")
        sdf_definition["sdfRef"] = convert_pointer(pointer, current_path)


def map_tm_required(
    wot_model: Dict,
    wot_definition: Dict,
    sdf_definition: Dict,
    current_path: str,
    mapped_fields: List[str],
):
    if "tm:required" in wot_definition:
        mapped_fields.append("tm:required")
        pointers = wot_definition["tm:required"]
        converted_pointers = [convert_pointer(x, current_path) for x in pointers]
        sdf_definition["sdfRequired"] = converted_pointers


def map_thing_model_to_sdf_object(
    thing_model: Dict,
    thing_model_key: str,
    sdf_definition,
    sdf_mapping_file,
    current_path: str,
    placeholder_map=None,
):
    sdf_object: Dict = {}

    # TODO: Deal with @context and @type
    mapped_fields: List[str] = [
        "@context",
        "@type",
        "sdf:defaultNamespace",
        "sdf:title",
        "sdf:copyright",
        "sdf:license",
    ]

    sdf_thing_key = thing_model.get("sdf:objectKey")
    if sdf_thing_key is not None:
        thing_model_key = sdf_thing_key
        mapped_fields.append("sdf:objectKey")
    elif thing_model_key is None:
        thing_model_key = f"sdfObject{len(sdf_definition)}"

    sdf_object_path = f"{current_path}/sdfObject/{thing_model_key}"

    map_title(thing_model, sdf_object, mapped_fields)
    map_description(thing_model, sdf_object, mapped_fields)
    map_links(thing_model, sdf_object, sdf_mapping_file, mapped_fields)
    map_version(thing_model, sdf_object, sdf_mapping_file, mapped_fields)

    map_sdf_comment(thing_model, sdf_object, mapped_fields)
    map_tm_required(
        thing_model, thing_model, sdf_object, sdf_object_path, mapped_fields
    )

    map_properties(
        thing_model, sdf_object, sdf_mapping_file, sdf_object_path, mapped_fields
    )
    map_actions(
        thing_model, sdf_object, sdf_mapping_file, sdf_object_path, mapped_fields
    )
    map_events(
        thing_model, sdf_object, sdf_mapping_file, sdf_object_path, mapped_fields
    )
    map_schema_definitions(
        thing_model, sdf_object, sdf_mapping_file, sdf_object_path, mapped_fields
    )

    map_additional_fields(sdf_mapping_file, thing_model, sdf_object_path, mapped_fields)

    sdf_definition[thing_model_key] = sdf_object


# TODO: Generalize
def determine_thing_model_key(
    thing_model, thing_model_key, sdf_definition, mapped_fields: List[str]
):
    sdf_thing_key = thing_model.get("sdf:thingKey")
    if sdf_thing_key is not None:
        thing_model_key = sdf_thing_key
        mapped_fields.append("sdf:thingKey")
    elif thing_model_key is None:
        thing_model_key = f"sdfThing{len(sdf_definition)}"

    return thing_model_key


def map_additional_field(
    mapping_file: dict, wot_definition: dict, current_sdf_path: str, key: str
):
    initialize_object_field(mapping_file, "map")
    map = mapping_file["map"]

    initialize_object_field(map, current_sdf_path)
    map[current_sdf_path][key] = wot_definition


def map_additional_fields(
    mapping_file: dict,
    wot_definition: dict,
    current_sdf_path: str,
    mapped_fields: List[str],
):

    for key, value in wot_definition.items():
        if key in mapped_fields:
            continue

        map_additional_field(mapping_file, value, current_sdf_path, key)


def map_thing_model_to_sdf_thing(
    thing_model: Dict,
    sub_models: Dict,
    thing_model_key: str,
    sdf_definition,
    sdf_mapping_file,
    current_path,
    placeholder_map=None,
    thing_model_collection=None,
):
    # TODO: Map @context, titles, descriptions of submodels?
    sdf_thing: Dict = {}
    mapped_fields: List[str] = [
        "@context",
        "@type",
        "sdf:defaultNamespace",
        "sdf:title",
        "sdf:copyright",
        "sdf:license",
    ]

    thing_model_key = determine_thing_model_key(
        thing_model, thing_model_key, sdf_definition, mapped_fields
    )

    sdf_thing_path = f"{current_path}/sdfThing/{thing_model_key}"

    map_tm_required(thing_model, thing_model, sdf_thing, sdf_thing_path, mapped_fields)

    map_title(thing_model, sdf_thing, mapped_fields)
    map_description(thing_model, sdf_thing, mapped_fields)
    map_links(thing_model, sdf_thing, sdf_mapping_file, mapped_fields)
    map_version(thing_model, sdf_thing, sdf_mapping_file, mapped_fields)

    map_sdf_comment(thing_model, sdf_thing, mapped_fields)

    map_properties(
        thing_model, sdf_thing, sdf_mapping_file, sdf_thing_path, mapped_fields
    )
    map_actions(thing_model, sdf_thing, sdf_mapping_file, sdf_thing_path, mapped_fields)
    map_events(thing_model, sdf_thing, sdf_mapping_file, sdf_thing_path, mapped_fields)
    map_schema_definitions(
        thing_model, sdf_thing, sdf_mapping_file, sdf_thing_path, mapped_fields
    )

    map_additional_fields(sdf_mapping_file, thing_model, sdf_thing_path, mapped_fields)

    sdf_definition[thing_model_key] = sdf_thing

    for key, value in sub_models.items():
        local_sub_models = resolve_sub_things(
            value,
            placeholder_map=placeholder_map,
            thing_collection=thing_model_collection,
        )
        map_thing_model(
            value,
            local_sub_models,
            key,
            sdf_thing,
            sdf_mapping_file,
            sdf_thing_path,
            placeholder_map=placeholder_map,
            thing_model_collection=thing_model_collection,
        )


def map_thing_model(
    thing_model: Dict,
    sub_models: Dict,
    thing_model_key,
    sdf_model,
    sdf_mapping_file,
    current_path: str,
    placeholder_map=None,
    thing_model_collection=None,
):
    if len(sub_models) > 0 or "sdf:thingKey" in thing_model:
        # TODO: Refactor into function
        initialize_object_field(sdf_model, "sdfThing")
        sdf_things = sdf_model["sdfThing"]

        map_thing_model_to_sdf_thing(
            thing_model,
            sub_models,
            thing_model_key,
            sdf_things,
            sdf_mapping_file,
            current_path,
            placeholder_map=placeholder_map,
            thing_model_collection=thing_model_collection,
        )
    else:
        # TODO: Refactor into function
        initialize_object_field(sdf_model, "sdfObject")
        sdf_objects = sdf_model["sdfObject"]

        map_thing_model_to_sdf_object(
            thing_model,
            thing_model_key,
            sdf_objects,
            sdf_mapping_file,
            current_path,
            placeholder_map=placeholder_map,
        )


def get_license_link(thing_model: Dict):
    for link in thing_model.get("links", []):
        if link.get("rel") == "license":
            return link

    return None


def map_infoblock_fields(thing_model, sdf_model):
    # TODO: How to deal with infoblock information in submodels?
    infoblock = {}

    map_field(thing_model, infoblock, "sdf:copyright", "copyright")

    license_link = get_license_link(thing_model)
    if license_link is not None:
        infoblock["license"] = license_link["href"]
    elif "sdf:license" in thing_model:
        infoblock["license"] = thing_model["sdf:license"]

    map_field(thing_model, infoblock, "sdf:title", "title")

    if "model" in thing_model.get("version", {}):
        infoblock["version"] = thing_model["version"]["model"]

    if len(infoblock) > 0:
        sdf_model["info"] = infoblock


def _get_submodel_key_from_link(link: Dict) -> str:
    key = link.get("instanceName")
    if key is None:
        href: str = link["href"]
        if href.startswith("#/"):
            href = href[1:]
        # TODO: Check if the actual map key should be the path/
        parsed_href = urllib.parse.urlparse(href)
        key = parsed_href.path
        key = os.path.split(key)[1]
        for file_extension in ["jsonld", "json", "tm", "td"]:
            key = key.replace(f".{file_extension}", "")
    return key


def resolve_sub_things(thing_model: Dict, thing_collection=None, placeholder_map=None):
    sub_models: Dict = {}

    for link in thing_model.get("links", []):
        if link.get("rel") == "tm:submodel":
            sub_model = retrieve_thing_model(
                link["href"], thing_collection=thing_collection
            )
            replace_placeholders(sub_model, placeholder_map)
            key = _get_submodel_key_from_link(link)
            sub_models[key] = sub_model

    return sub_models


def convert_wot_tm_to_sdf(
    thing_model: Dict,
    thing_model_key=None,
    placeholder_map=None,
    thing_model_collection=None,
    top_model_keys: Union[Set[str], None] = None,
) -> Union[Dict, Tuple[Dict, Dict]]:
    if is_thing_collection(thing_model):
        return convert_wot_tm_collection_to_sdf(
            thing_model,
            top_model_keys=top_model_keys,
        )

    sdf_model: Dict = {}
    sdf_mapping_file: Dict = {}

    thing_model = resolve_extension(thing_model, resolve_relative_pointers=False)
    thing_model = replace_placeholders(thing_model, placeholder_map)

    # TODO: @context of submoduls needs to be integrated as well
    # TODO: Revisit context mappings
    map_context(thing_model, sdf_model, sdf_mapping_file)
    map_infoblock_fields(thing_model, sdf_model)

    # TODO: This distinction needs to be revisited
    if top_model_keys is None or len(top_model_keys) == 0:
        sub_models = resolve_sub_things(
            thing_model,
            thing_collection=thing_model_collection,
            placeholder_map=placeholder_map,
        )
        map_thing_model(
            thing_model,
            sub_models,
            thing_model_key,
            sdf_model,
            sdf_mapping_file,
            "#",
            placeholder_map=placeholder_map,
            thing_model_collection=thing_model_collection,
        )
    else:
        top_level_models = [thing_model_collection[x] for x in top_model_keys]

        for model, key in zip(top_level_models, top_model_keys):
            sub_models = resolve_sub_things(
                model,
                thing_collection=thing_model_collection,
                placeholder_map=placeholder_map,
            )
            map_thing_model(
                model,
                sub_models,
                key,
                sdf_model,
                sdf_mapping_file,
                "#",
                placeholder_map=placeholder_map,
                thing_model_collection=thing_model_collection,
            )

    validate_sdf_model(sdf_model)

    if sdf_mapping_file.get("map") is not None:
        for field_name in ["info", "namespace", "defaultNamespace"]:
            field = sdf_model.get(field_name)
            if field is None:
                continue
            sdf_mapping_file[field_name] = copy.deepcopy(field)

        return sdf_model, sdf_mapping_file

    return sdf_model


def _get_submodel_keys(thing_model: Dict):
    links = thing_model.get("links", [])
    submodel_links = [
        link["href"] for link in links if link.get("rel") == "tm:submodel"
    ]
    submodel_keys = [link[2:] for link in submodel_links if link.startswith("#/")]
    return submodel_keys


def detect_top_level_models(thing_model_collection: Dict):
    referenced_models = set()
    for thing_model in thing_model_collection.values():
        for key in _get_submodel_keys(thing_model):
            referenced_models.add(key)
    return {
        key for key in thing_model_collection.keys() if key not in referenced_models
    }


def convert_wot_tm_collection_to_sdf(
    thing_model_collection: Dict,
    root_model_key=None,
    top_model_keys: Union[Set[str], None] = None,
) -> Union[Dict, Tuple[Dict, Dict]]:

    if top_model_keys is None:
        top_model_keys = detect_top_level_models(thing_model_collection)

    if root_model_key is not None:
        root_model = thing_model_collection[root_model_key]
        top_model_keys.add(root_model_key)
    else:
        # Use the first top-level model in the map as default
        root_model_key = list(top_model_keys)[0]
        root_model = thing_model_collection[root_model_key]

    return convert_wot_tm_to_sdf(
        root_model,
        thing_model_key=root_model_key,
        thing_model_collection=thing_model_collection,
        top_model_keys=top_model_keys,
    )
