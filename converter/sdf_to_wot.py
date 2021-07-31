from typing import Any, Dict, List, Optional
from jsonpointer import resolve_pointer
import json_merge_patch
import urllib.request
from urllib.error import HTTPError, URLError
import json


def resolve_namespace(sdf_model: dict, namespace: Optional[str]):
    if not namespace:
        namespace = sdf_model.get("defaultNamespace", "#")
    return namespace


def resolve_sdf_ref(sdf_model: Dict, sdf_definition: Dict, namespace: Optional[str], sdf_ref_list: List[str]):
    # TODO: This function should be reworked

    if "sdfRef" in sdf_definition:
        sdf_ref = sdf_definition["sdfRef"]
        root, pointer = tuple(sdf_ref.split("/", 1))

        namespace = resolve_namespace(sdf_model, namespace)
        resolved_sdf_ref = sdf_ref.replace("#", namespace)

        if resolved_sdf_ref in sdf_ref_list:
            return sdf_definition
        if root == "#":
            original = resolve_pointer(sdf_model, "/" + pointer)
            original = resolve_sdf_ref(
                sdf_model, original, namespace, sdf_ref_list + [resolved_sdf_ref])
        elif root.endswith(":"):
            root = root[:-1]
            resolved_url = sdf_model.get("namespace", {}).get(root)
            try:
                with urllib.request.urlopen(resolved_url) as url:
                    retrieved_sdf_model = json.loads(url.read().decode())
                    original = resolve_pointer(
                        retrieved_sdf_model, "/" + pointer)
                    original = resolve_sdf_ref(
                        retrieved_sdf_model, original, resolved_url, sdf_ref_list)
            except (AttributeError, HTTPError, URLError):
                return sdf_definition
        else:
            return sdf_definition

        return json_merge_patch.merge(original, sdf_definition)
    return sdf_definition


def initialize_object_field(model: Dict, field_name: str):
    if field_name not in model:
        model[field_name] = {}


def initialize_list_field(model: Dict, field_name: str):
    if field_name not in model:
        model[field_name] = []


def map_namespace(sdf_model: Dict, thing_model: Dict):
    namespaces = sdf_model.get("namespace", {}).copy()
    namespaces["sdf"] = "https://example.com/sdf"
    thing_model["@context"].append(namespaces)


def create_link(href: str, type: Optional[str],  rel: Optional[str],  anchor: Optional[str],  sizes: Optional[str]) -> Dict:
    link = {"href": href}

    for key, value in [("type", type), ("rel", rel), ("anchor", anchor), ("sizes", sizes)]:
        if value is not None:
            link[key] = value

    return link


def add_link(thing_model: Dict, href: str, type: Optional[str],  rel: Optional[str],  anchor: Optional[str],  sizes: Optional[str]):
    initialize_list_field(thing_model, "links")

    link = create_link(href, type, rel, anchor, sizes)
    thing_model["links"].append(link)


def map_license(infoblock: Dict, thing_model: Dict):
    license_href = infoblock.get("license")
    if license_href:
        pass
        # add_link(thing_model, license_href, None, "license", None, None)


def map_version(infoblock: Dict, thing_model: Dict):
    version = infoblock.get("version")
    if version:
        thing_model["version"] = {"instance": version}


def map_infoblock(sdf_model: Dict, thing_model: Dict):
    infoblock = sdf_model.get("info")
    if infoblock:
        map_field(infoblock, thing_model, "label", "title")
        map_field(infoblock, thing_model, "copyright", "description")
        map_license(infoblock, thing_model)
        map_version(infoblock, thing_model)


def map_field(sdf_definition: Dict, wot_definition: Dict, sdf_key: str, wot_key: str):
    if sdf_key in sdf_definition:
        wot_definition[wot_key] = sdf_definition[sdf_key]


def map_common_qualities(sdf_definition: Dict, wot_definition: Dict):
    map_field(sdf_definition, wot_definition, "label", "title")
    map_field(sdf_definition, wot_definition, "description", "description")
    map_field(sdf_definition, wot_definition, "$comment", "sdf:$comment")


def map_data_qualities(sdf_model: Dict, data_qualities: Dict, data_schema: Dict, is_property=False):
    # TODO: Unmapped fields: sdfChoice, nullable, sdfType, contentFormat

    data_qualities = resolve_sdf_ref(sdf_model, data_qualities, None, [])

    map_common_qualities(data_qualities, data_schema)

    for sdf_field, wot_field in [("writeable", "readOnly"), ("readable", "writeOnly")]:
        if sdf_field in data_qualities:
            data_schema[wot_field] = not data_qualities[sdf_field]

    for field_name in ["type", "unit", "enum", "const", "default", "multipleOf", "minLength",
                       "maxLength", "minItems", "maxItems", "minimum", "maximum",
                       "multipleOf", "required", "format", "uniqueItems", "pattern",
                       "exclusiveMinimum", "exclusiveMaximum"]:
        map_field(data_qualities, data_schema, field_name, field_name)

    if is_property:
        map_field(data_qualities, data_schema, "observable", "observable")
    else:
        map_field(data_qualities, data_schema, "observable", "sdf:observable")

    if "items" in data_qualities:
        data_schema["items"] = {}
        map_data_qualities(sdf_model,
                           data_qualities["items"],
                           data_schema["items"]
                           )

    for key, property in data_qualities.get("properties", {}).items():
        initialize_object_field(data_schema, "properties")
        data_schema["properties"][key] = {}
        map_data_qualities(sdf_model, property, data_schema["properties"][key])


def map_action_qualities(sdf_model: Dict, thing_model: Dict, sdf_action: Dict, affordance_key: str, json_pointer: str):
    initialize_object_field(thing_model, "actions")

    wot_action: Dict[str, Any] = {
        "sdf:jsonPointer": json_pointer
    }
    collect_sdf_required(thing_model, sdf_action)

    map_common_qualities(sdf_action, wot_action)

    data_map_pairs = [("sdfInputData", "input"),
                      ("sdfOutputData", "output")]

    for sdf_field, wot_field in data_map_pairs:
        if sdf_field in sdf_action:
            wot_action[wot_field] = {}
            map_data_qualities(sdf_model, sdf_action[sdf_field], wot_action[wot_field])

    thing_model["actions"][affordance_key] = wot_action


def map_property_qualities(sdf_model: Dict, thing_model: Dict, sdf_property: Dict, affordance_key: str, json_pointer: str):
    initialize_object_field(thing_model, "properties")

    wot_property: Dict[str, Any] = {
        "sdf:jsonPointer": json_pointer
    }
    collect_sdf_required(thing_model, sdf_property)

    map_data_qualities(sdf_model, sdf_property, wot_property, is_property=True)

    thing_model["properties"][affordance_key] = wot_property


def map_sdf_action(sdf_model: Dict, sdf_definition: Dict, thing_model: Dict, prefix_list: List[str], json_pointer_prefix: str):
    for key, sdf_action in sdf_definition.get("sdfAction", {}).items():
        affordance_key = "_".join(prefix_list + [key])
        map_action_qualities(sdf_model, thing_model, sdf_action,
                             affordance_key, f"{json_pointer_prefix}/sdfAction/{key}")


def map_object_qualities(sdf_model: Dict, sdf_definition: Dict, thing_model: Dict, prefix_list: List[str], json_pointer_prefix: str):
    for key, sdf_object in sdf_definition.get("sdfObject", {}).items():
        # TODO: Check if this actually works
        collect_sdf_required(thing_model, sdf_object)
        sdf_object = resolve_sdf_ref(sdf_model, sdf_object, None, [])
        appended_prefix = f"{json_pointer_prefix}/sdfObject/{key}"
        map_sdf_action(sdf_model, sdf_object, thing_model,
                       prefix_list + [key], appended_prefix)
        map_sdf_property(sdf_model, sdf_object, thing_model,
                         prefix_list + [key], appended_prefix)
        map_sdf_event(sdf_model, sdf_object, thing_model,
                      prefix_list + [key], appended_prefix)


def map_thing_qualities(sdf_model: Dict, sdf_definition: Dict, thing_model: Dict, prefix_list: List[str], json_pointer_prefix: str):
    for key, sdf_thing in sdf_definition.get("sdfThing", {}).items():
        # TODO: Check if this actually works
        collect_sdf_required(thing_model, sdf_thing)
        sdf_thing = resolve_sdf_ref(sdf_model, sdf_thing, None, [])
        pointer_prefix = f"{json_pointer_prefix}/sdfThing/{key}"
        map_thing_qualities(sdf_model, sdf_thing, thing_model,
                            prefix_list + [key], pointer_prefix)
        map_object_qualities(sdf_model, sdf_thing, thing_model,
                             prefix_list + [key], pointer_prefix)


def map_sdf_property(sdf_model: Dict, sdf_definition: Dict, thing_model: Dict, prefix_list: List[str], json_pointer_prefix: str):
    for key, sdf_property in sdf_definition.get("sdfProperty", {}).items():
        affordance_key = "_".join(prefix_list + [key])
        map_property_qualities(sdf_model, thing_model, sdf_property,
                               affordance_key, f"{json_pointer_prefix}/sdfProperty/{key}")


def map_event_qualities(sdf_model: Dict, thing_model: Dict, sdf_event: Dict, affordance_key: str, json_pointer: str):
    initialize_object_field(thing_model, "actions")

    wot_event: Dict[str, Any] = {
        "sdf:jsonPointer": json_pointer
    }
    collect_sdf_required(thing_model, sdf_event)

    map_common_qualities(sdf_event, wot_event)

    if "sdfOutputData" in sdf_event:
        wot_event["data"] = {}
        map_data_qualities(
            sdf_model, sdf_event["sdfOutputData"], wot_event["data"])

    thing_model["events"][affordance_key] = wot_event


def collect_sdf_required(thing_model: Dict, sdf_definition: Dict):
    thing_model["sdfRequired"].extend(sdf_definition.get("sdfRequired", []))


def map_sdf_event(sdf_model: Dict, sdf_definition: Dict, thing_model: Dict, prefix_list: List[str], json_pointer_prefix: str):
    for key, sdf_event in sdf_definition.get("sdfEvent", {}).items():
        affordance_key = "_".join(prefix_list + [key])
        map_property_qualities(sdf_model, thing_model, sdf_event,
                               affordance_key, f"{json_pointer_prefix}/sdfEvent/{key}")


def map_sdf_required(thing_model: Dict):
    initialize_list_field(thing_model, "tm:required")
    for affordance_type in ["actions", "properties", "events"]:
        for key, value in thing_model.get(affordance_type, {}).items():
            if "sdf:jsonPointer" in value:
                json_pointer = value["sdf:jsonPointer"]
                if json_pointer in thing_model.get("sdfRequired", []):
                    thing_model["tm:required"].append(
                        f"#/{affordance_type}/{key}")
    if not thing_model["tm:required"]:
        del thing_model["tm:required"]


def convert_sdf_to_wot_tm(sdf_model: Dict) -> Dict:

    thing_model: Dict = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": "tm:ThingModel",
        "sdfRequired": []
    }

    map_infoblock(sdf_model, thing_model)
    map_namespace(sdf_model, thing_model)

    map_thing_qualities(sdf_model, sdf_model, thing_model, [], "#")
    map_object_qualities(sdf_model, sdf_model, thing_model, [], "#")

    map_sdf_action(sdf_model, sdf_model, thing_model, [], "#")
    map_sdf_property(sdf_model, sdf_model, thing_model, [], "#")
    map_sdf_event(sdf_model, sdf_model, thing_model, [], "#")

    map_sdf_required(thing_model)
    del thing_model["sdfRequired"]

    return thing_model
