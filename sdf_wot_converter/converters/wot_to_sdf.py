import os
from typing import (
    Any,
    Dict,
    Set,
    Union,
)
import warnings

import jsonschema

from .common.jsonschema import (
    map_common_json_schema_fields,
)
from .utility import (
    initialize_list_field,
    initialize_object_field,
    map_field,
    map_common_field,
    validate_sdf_model,
)
from . import wot_common
import urllib.parse


def map_properties(
    thing_model: Dict, sdf_model: Dict, sdf_mapping_file, current_path: str
):
    for key, wot_property in thing_model.get("properties", {}).items():
        initialize_object_field(sdf_model, "sdfProperty")
        sdf_property: Dict[str, Any] = {}
        map_interaction_affordance_fields(wot_property, sdf_property)
        map_data_schema_fields(
            thing_model, wot_property, sdf_property, current_path, is_property=True
        )
        map_observable(wot_property, sdf_property)

        sdf_model["sdfProperty"][key] = sdf_property


def map_items(
    thing_model, wot_definition: Dict, sdf_definition: Dict, current_path: str
):
    if "items" in wot_definition:
        sdf_definition["items"] = {}
        map_data_schema_fields(
            thing_model, wot_definition["items"], sdf_definition["items"], current_path
        )


def map_dataschema_properties(
    thing_model, wot_definition: Dict, sdf_definition: Dict, current_path: str
):
    for key, property in wot_definition.get("properties", {}).items():
        initialize_object_field(sdf_definition, "properties")
        sdf_definition["properties"][key] = {}
        map_data_schema_fields(
            thing_model, property, sdf_definition["properties"][key], current_path
        )


def map_actions(
    thing_model: Dict, sdf_model: Dict, sdf_mapping_file, current_path: str
):
    for key, wot_action in thing_model.get("actions", {}).items():
        initialize_object_field(sdf_model, "sdfAction")
        sdf_action: Dict[str, Any] = {}
        map_sdf_comment(wot_action, sdf_action)
        map_interaction_affordance_fields(wot_action, sdf_action)
        map_action_fields(thing_model, wot_action, sdf_action, current_path)
        map_tm_ref(thing_model, wot_action, sdf_action, current_path)
        sdf_model["sdfAction"][key] = sdf_action


def map_action_fields(thing_model, wot_action, sdf_action, current_path: str):
    # TODO: Missing fields: safe, idempotent
    if "input" in wot_action:
        sdf_input_data: Dict[str, Any] = {}
        map_data_schema_fields(
            thing_model, wot_action["input"], sdf_input_data, current_path
        )
        sdf_action["sdfInputData"] = sdf_input_data
    if "output" in wot_action:
        sdf_output_data: Dict[str, Any] = {}
        map_data_schema_fields(
            thing_model, wot_action["output"], sdf_output_data, current_path
        )
        sdf_action["sdfOutputData"] = sdf_output_data


def map_events(thing_model: Dict, sdf_model: Dict, sdf_mapping_file, current_path: str):
    for key, wot_event in thing_model.get("events", {}).items():
        initialize_object_field(sdf_model, "sdfEvent")
        sdf_event: Dict[str, Any] = {}
        map_sdf_comment(wot_event, sdf_event)
        map_interaction_affordance_fields(wot_event, sdf_event)
        map_event_fields(thing_model, wot_event, sdf_event, current_path)
        map_tm_ref(thing_model, wot_event, sdf_event, current_path)
        sdf_model["sdfEvent"][key] = sdf_event


def map_event_fields(thing_model, wot_event, sdf_event, current_path: str):
    # TODO: Missing fields: subscription, cancellation
    if "data" in wot_event:
        sdf_input_data: Dict = {}
        map_data_schema_fields(
            thing_model, wot_event["data"], sdf_input_data, current_path
        )
        sdf_event["sdfOutputData"] = sdf_input_data


def map_data_schema_fields(
    thing_model,
    wot_definition: Dict,
    sdf_definition: Dict,
    current_path: str,
    is_property=False,
):
    # TODO: Unmapped fields: @type, titles, descriptions, oneOf,
    # TODO: Deal with sdfType and nullable
    map_sdf_comment(wot_definition, sdf_definition)

    map_common_json_schema_fields(wot_definition, sdf_definition)

    map_title(wot_definition, sdf_definition)
    map_description(wot_definition, sdf_definition)
    map_enum(wot_definition, sdf_definition)
    if is_property:
        # TODO: Add mapping for when not part of dataschema
        map_read_only(wot_definition, sdf_definition)
        map_write_only(wot_definition, sdf_definition)
    map_unique_items(wot_definition, sdf_definition)
    map_content_format(wot_definition, sdf_definition)

    map_items(thing_model, wot_definition, sdf_definition, current_path)
    map_dataschema_properties(thing_model, wot_definition, sdf_definition, current_path)

    map_tm_ref(thing_model, wot_definition, sdf_definition, current_path)


def map_unique_items(wot_definition: Dict, sdf_definition: Dict):
    map_common_field(wot_definition, sdf_definition, "uniqueItems")


def map_content_format(wot_definition: Dict, sdf_definition: Dict):
    map_field(wot_definition, sdf_definition, "contentMediaType", "contentFormat")


def map_enum(wot_definition: Dict, sdf_definition: Dict):
    if "enum" in wot_definition:
        for enum in wot_definition["enum"]:
            if type(enum) is dict and "sdf:choiceName" in enum:
                initialize_object_field(sdf_definition, "sdfChoice")
                choice_name = enum["sdf:choiceName"]
                sdf_definition["sdfChoice"][choice_name] = enum
                del sdf_definition["sdfChoice"][choice_name]["sdf:choiceName"]
            else:
                initialize_list_field(sdf_definition, "enum")
                sdf_definition["enum"].append(enum)


def map_read_only(wot_definition: Dict, sdf_definition: Dict):
    if "readOnly" in wot_definition:
        sdf_definition["writable"] = not wot_definition["readOnly"]


def map_write_only(wot_definition: Dict, sdf_definition: Dict):
    if "writeOnly" in wot_definition:
        sdf_definition["readable"] = not wot_definition["writeOnly"]


def map_observable(wot_property: Dict, sdf_property: Dict):
    sdf_property["observable"] = wot_property.get("observable", False)


def map_interaction_affordance_fields(wot_definition: Dict, sdf_definition: Dict):
    # TODO: Unmapped fields: @type, titles, descriptions, forms, uriVariables
    map_title(wot_definition, sdf_definition)
    map_description(wot_definition, sdf_definition)


def map_title(wot_definition: Dict, sdf_definition: Dict):
    map_field(wot_definition, sdf_definition, "title", "label")


def map_description(wot_definition: Dict, sdf_definition: Dict):
    map_common_field(wot_definition, sdf_definition, "description")


def map_schema_definitions(
    thing_model: Dict, sdf_model: Dict, sdf_mapping_file, current_path: str
):
    for key, wot_schema_definitions in thing_model.get("schemaDefinitions", {}).items():
        if "sdfData" not in sdf_model:
            sdf_model["sdfData"] = {}
        sdf_data: Dict[str, Any] = {}
        map_sdf_comment(wot_schema_definitions, sdf_data)
        map_data_schema_fields(
            thing_model, wot_schema_definitions, sdf_data, current_path
        )
        map_tm_ref(thing_model, wot_schema_definitions, sdf_data, current_path)

        sdf_model["sdfData"][key] = sdf_data


def map_links(wot_definition: Dict, sdf_definition: Dict, sdf_mapping_file):
    # TODO: Deal with other link types
    for link in wot_definition.get("links", []):
        if link.get("rel") == "license":
            continue


def map_version(wot_definition: Dict, sdf_definition: Dict, sdf_mapping_file: Dict):
    version_info = wot_definition.get("version", {})
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


def map_sdf_comment(wot_definition: Dict, sdf_definition: Dict):
    # TODO: Move somewhere else
    if "sdf:$comment" in wot_definition:
        sdf_definition["$comment"] = wot_definition["sdf:$comment"]


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
    wot_model: Dict, wot_definition: Dict, sdf_definition: Dict, current_path: str
):
    if "tm:ref" in wot_definition:
        pointer = wot_definition["tm:ref"]
        sdf_definition["sdfRef"] = convert_pointer(pointer, current_path)


def map_tm_required(
    wot_model: Dict, wot_definition: Dict, sdf_definition: Dict, current_path: str
):
    if "tm:required" in wot_definition:
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

    sdf_thing_key = thing_model.get("sdf:objectKey")
    if sdf_thing_key is not None:
        thing_model_key = sdf_thing_key
    elif thing_model_key is None:
        thing_model_key = f"sdfObject{len(sdf_definition)}"

    sdf_object_path = f"{current_path}/sdfObject/{thing_model_key}"

    map_title(thing_model, sdf_object)
    map_description(thing_model, sdf_object)
    map_links(thing_model, sdf_object, sdf_mapping_file)
    map_version(thing_model, sdf_object, sdf_mapping_file)

    map_sdf_comment(thing_model, sdf_object)
    map_tm_required(thing_model, thing_model, sdf_object, sdf_object_path)

    map_properties(thing_model, sdf_object, sdf_mapping_file, sdf_object_path)
    map_actions(thing_model, sdf_object, sdf_mapping_file, sdf_object_path)
    map_events(thing_model, sdf_object, sdf_mapping_file, sdf_object_path)
    map_schema_definitions(thing_model, sdf_object, sdf_mapping_file, sdf_object_path)

    sdf_definition[thing_model_key] = sdf_object


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

    sdf_thing_key = thing_model.get("sdf:thingKey")
    if sdf_thing_key is not None:
        thing_model_key = sdf_thing_key
    elif thing_model_key is None:
        thing_model_key = f"sdfThing{len(sdf_definition)}"

    sdf_thing_path = f"{current_path}/sdfThing/{thing_model_key}"

    map_tm_required(thing_model, thing_model, sdf_thing, sdf_thing_path)

    map_title(thing_model, sdf_thing)
    map_description(thing_model, sdf_thing)
    map_links(thing_model, sdf_thing, sdf_mapping_file)
    map_version(thing_model, sdf_thing, sdf_mapping_file)

    map_sdf_comment(thing_model, sdf_thing)

    map_properties(thing_model, sdf_thing, sdf_mapping_file, sdf_thing_path)
    map_actions(thing_model, sdf_thing, sdf_mapping_file, sdf_thing_path)
    map_events(thing_model, sdf_thing, sdf_mapping_file, sdf_thing_path)
    map_schema_definitions(thing_model, sdf_thing, sdf_mapping_file, sdf_thing_path)

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
        sdf_things = sdf_model.get("sdfThing")
        if sdf_things is None:
            sdf_things = {}
            sdf_model["sdfThing"] = sdf_things
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
        sdf_objects = sdf_model.get("sdfObject")
        if sdf_objects is None:
            sdf_objects = {}
            sdf_model["sdfObject"] = sdf_objects
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
            sub_model = wot_common.retrieve_thing_model(
                link["href"], thing_collection=thing_collection
            )
            wot_common.replace_placeholders(sub_model, placeholder_map)
            key = _get_submodel_key_from_link(link)
            sub_models[key] = sub_model

    return sub_models


def convert_wot_tm_to_sdf(
    thing_model: Dict,
    thing_model_key=None,
    placeholder_map=None,
    thing_model_collection=None,
    top_model_keys: Union[Set[str], None] = None,
) -> Dict:
    if thing_model_collection is None and "@context" not in thing_model:
        return convert_wot_tm_collection_to_sdf(
            thing_model,
            top_model_keys=top_model_keys,
        )

    # TODO: Unmapped fields: @type, id, titles, descriptions, created,
    #       modified, support, base, forms, security,
    #       securityDefinitions, profile, schemaDefinitions
    sdf_model: Dict = {}
    # TODO: Pass mapping file to conversion functions
    sdf_mapping_file: Dict = {}

    thing_model = wot_common.resolve_extension(
        thing_model, resolve_relative_pointers=False
    )
    thing_model = wot_common.replace_placeholders(thing_model, placeholder_map)

    # TODO: @context of submoduls needs to be integrated as well
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

    # TODO: Schema needs to be updated.
    try:
        validate_sdf_model(sdf_model)
    except jsonschema.exceptions.ValidationError:
        warnings.warn(
            "Conversion produced an invalid SDF model. "
            "This might be the case because the SDF schema "
            "has not been updated, yet."
            "It is recommended that you check the result before using it."
        )

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
):

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
