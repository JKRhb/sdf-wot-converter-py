from typing import (
    Any,
    Dict,
    List,
    Optional,
)
from jsonpointer import resolve_pointer
import json_merge_patch
import urllib.request
from .utility import (
    initialize_list_field,
    initialize_object_field,
)
import json


class SdfRefLoopError(Exception):
    """Raised when an sdfRef cannot be resolved due to a loop"""

    pass


class InvalidSdfRefError(Exception):
    """Raised when an unparsable sdfRef has been included in an SDF Model"""

    pass


class SdfRefUrlRetrievalError(Exception):
    """Raised when an sdfRef pointing to a URL could not be resolved"""

    pass


def resolve_namespace(sdf_model: dict, namespace: Optional[str]):
    if not namespace:
        namespace = sdf_model.get("defaultNamespace", "#")
    return namespace


def resolve_sdf_ref(
    sdf_model: Dict,
    sdf_definition: Dict,
    namespace: Optional[str],
    sdf_ref_list: List[str],
):
    # TODO: This function should be reworked

    if "sdfRef" in sdf_definition:
        sdf_ref = sdf_definition["sdfRef"]
        root, pointer = tuple(sdf_ref.split("/", 1))

        namespace = resolve_namespace(sdf_model, namespace)
        resolved_sdf_ref = sdf_ref.replace("#", namespace)

        if resolved_sdf_ref in sdf_ref_list:
            raise SdfRefLoopError(f"Encountered a looping sdfRef: {resolved_sdf_ref}")
        if root == "#":
            original = resolve_pointer(sdf_model, "/" + pointer)
            original = resolve_sdf_ref(
                sdf_model, original, namespace, sdf_ref_list + [resolved_sdf_ref]
            )
        elif root.endswith(":"):
            root = root[:-1]
            resolved_url = sdf_model.get("namespace", {}).get(root)
            try:
                with urllib.request.urlopen(resolved_url) as url:
                    retrieved_sdf_model = json.loads(url.read().decode())
                    original = resolve_pointer(retrieved_sdf_model, "/" + pointer)
                    original = resolve_sdf_ref(
                        retrieved_sdf_model, original, resolved_url, sdf_ref_list
                    )
            except Exception:
                raise SdfRefUrlRetrievalError(
                    f"No valid SDF model could be retrieved from {resolved_url}"
                )

            return json_merge_patch.merge(original, sdf_definition)
        else:
            raise InvalidSdfRefError(f"sdfRef {resolved_sdf_ref} could not be resolved")

    return sdf_definition


def map_namespace(sdf_model: Dict, thing_model: Dict):
    namespaces = sdf_model.get("namespace", {}).copy()
    namespaces["sdf"] = "https://example.com/sdf"
    thing_model["@context"].append(namespaces)


def map_default_namespace(sdf_model: Dict, thing_model: Dict):
    map_field(sdf_model, thing_model, "defaultNamespace", "sdf:defaultNamespace")


def create_link(
    href: str,
    type: Optional[str],
    rel: Optional[str],
    anchor: Optional[str],
    sizes: Optional[str],
) -> Dict:
    link = {"href": href}

    for key, value in [
        ("type", type),
        ("rel", rel),
        ("anchor", anchor),
        ("sizes", sizes),
    ]:
        if value is not None:
            link[key] = value

    return link


def add_link(
    thing_model: Dict,
    href: str,
    type: Optional[str],
    rel: Optional[str],
    anchor: Optional[str],
    sizes: Optional[str],
):
    initialize_list_field(thing_model, "links")

    link = create_link(href, type, rel, anchor, sizes)
    thing_model["links"].append(link)


def map_license(infoblock: Dict, thing_model: Dict):
    license_href = infoblock["license"]
    add_link(thing_model, license_href, None, "license", None, None)


def map_version(infoblock: Dict, thing_model: Dict):
    version = infoblock["version"]
    thing_model["version"] = {"model": version}


def map_infoblock(sdf_model: Dict, thing_model: Dict):
    infoblock = sdf_model.get("info")
    if infoblock:
        map_title(thing_model, infoblock)
        map_copyright(thing_model, infoblock)
        map_license(infoblock, thing_model)
        map_version(infoblock, thing_model)


def map_copyright(thing_model, infoblock):
    map_field(infoblock, thing_model, "copyright", "description")


def map_title(thing_model, infoblock):
    map_field(infoblock, thing_model, "title", "title")


def map_field(sdf_definition: Dict, wot_definition: Dict, sdf_key: str, wot_key: str):
    if sdf_key in sdf_definition:
        wot_definition[wot_key] = sdf_definition[sdf_key]


def map_common_qualities(sdf_definition: Dict, wot_definition: Dict):
    map_label(sdf_definition, wot_definition)
    map_description(sdf_definition, wot_definition)
    map_comment(sdf_definition, wot_definition)
    copy_sdf_ref(sdf_definition, wot_definition)


def copy_sdf_ref(sdf_definition, wot_definition):
    sdf_ref = sdf_definition.get("sdfRef")
    if sdf_ref and sdf_ref.startswith("#"):
        wot_definition["tm:ref"] = sdf_definition["sdfRef"]


def map_comment(sdf_definition, wot_definition):
    map_field(sdf_definition, wot_definition, "$comment", "sdf:$comment")


def map_description(sdf_definition, wot_definition):
    map_field(sdf_definition, wot_definition, "description", "description")


def map_label(sdf_definition: Dict, wot_definition: Dict):
    map_field(sdf_definition, wot_definition, "label", "title")


def map_sdf_choice(sdf_model: Dict, data_qualities: Dict, data_schema: Dict):
    if "sdfChoice" in data_qualities:
        initialize_list_field(data_schema, "enum")
        for choice_name, choice in data_qualities["sdfChoice"].items():
            mapped_choice = {"sdf:choiceName": choice_name}
            map_data_qualities(sdf_model, choice, mapped_choice)
            data_schema["enum"].append(mapped_choice)


def map_data_qualities(
    sdf_model: Dict, data_qualities: Dict, data_schema: Dict, is_property=False
):
    data_qualities = resolve_sdf_ref(sdf_model, data_qualities, None, [])

    map_common_qualities(data_qualities, data_schema)

    for sdf_field, wot_field in [("writable", "readOnly"), ("readable", "writeOnly")]:
        if sdf_field in data_qualities:
            data_schema[wot_field] = not data_qualities[sdf_field]

    map_jsonschema_type(data_qualities, data_schema)
    map_unit(data_qualities, data_schema)
    map_enum(data_qualities, data_schema)
    map_const(data_qualities, data_schema)
    map_default(data_qualities, data_schema)
    map_multiple_of(data_qualities, data_schema)
    map_min_length(data_qualities, data_schema)
    map_max_length(data_qualities, data_schema)
    map_min_items(data_qualities, data_schema)
    map_max_items(data_qualities, data_schema)
    map_minimum(data_qualities, data_schema)
    map_maximum(data_qualities, data_schema)
    map_required(data_qualities, data_schema)
    map_format(data_qualities, data_schema)
    map_unique_items(data_qualities, data_schema)
    map_pattern(data_qualities, data_schema)
    map_exclusive_minimum(data_qualities, data_schema)
    map_exclusive_maximum(data_qualities, data_schema)
    map_content_format(data_qualities, data_schema)

    # TODO: Revisit the mapping of these two fields
    map_nullable(data_qualities, data_schema)
    map_sdf_type(data_qualities, data_schema)

    map_sdf_choice(sdf_model, data_qualities, data_schema)

    map_observable(data_qualities, data_schema, is_property)

    map_items(sdf_model, data_qualities, data_schema)

    map_properties(sdf_model, data_qualities, data_schema)


def map_properties(sdf_model, data_qualities, data_schema):
    for key, property in data_qualities.get("properties", {}).items():
        initialize_object_field(data_schema, "properties")
        data_schema["properties"][key] = {}
        map_data_qualities(sdf_model, property, data_schema["properties"][key])


def map_items(sdf_model, data_qualities, data_schema):
    if "items" in data_qualities:
        data_schema["items"] = {}
        map_data_qualities(sdf_model, data_qualities["items"], data_schema["items"])


def map_observable(data_qualities, data_schema, is_property):
    if is_property:
        map_field(data_qualities, data_schema, "observable", "observable")
    else:
        map_field(data_qualities, data_schema, "observable", "sdf:observable")


def map_sdf_type(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "sdfType", "sdf:sdfType")


def map_nullable(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "nullable", "sdf:nullable")


def map_content_format(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "contentFormat", "contentMediaType")


def map_exclusive_maximum(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "exclusiveMaximum", "exclusiveMaximum")


def map_exclusive_minimum(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "exclusiveMinimum", "exclusiveMinimum")


def map_pattern(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "pattern", "pattern")


def map_unique_items(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "uniqueItems", "uniqueItems")


def map_format(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "format", "format")


def map_required(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "required", "required")


def map_maximum(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "maximum", "maximum")


def map_minimum(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "minimum", "minimum")


def map_max_items(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "maxItems", "maxItems")


def map_min_items(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "minItems", "minItems")


def map_max_length(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "maxLength", "maxLength")


def map_min_length(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "minLength", "minLength")


def map_multiple_of(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "multipleOf", "multipleOf")


def map_default(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "default", "default")


def map_const(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "const", "const")


def map_enum(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "enum", "enum")


def map_unit(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "unit", "unit")


def map_jsonschema_type(data_qualities, data_schema):
    map_field(data_qualities, data_schema, "type", "type")


def map_action_qualities(
    sdf_model: Dict,
    thing_model: Dict,
    sdf_action: Dict,
    prefix_list: List[str],
    json_pointer: str,
):
    initialize_object_field(thing_model, "actions")
    affordance_key = "_".join(prefix_list)

    wot_action = create_wot_affordance(json_pointer)
    collect_sdf_required(thing_model, sdf_action)
    collect_mapping(thing_model, json_pointer, "actions", affordance_key)
    sdf_action = resolve_sdf_ref(sdf_model, sdf_action, None, [])

    map_common_qualities(sdf_action, wot_action)

    data_map_pairs = [("sdfInputData", "input"), ("sdfOutputData", "output")]

    for sdf_field, wot_field in data_map_pairs:
        if sdf_field in sdf_action:
            wot_action[wot_field] = {}
            map_data_qualities(sdf_model, sdf_action[sdf_field], wot_action[wot_field])

    map_sdf_data(
        sdf_model, sdf_action, thing_model, prefix_list, json_pointer, suffix="action"
    )

    thing_model["actions"][affordance_key] = wot_action


def create_wot_affordance(json_pointer):
    wot_action: Dict[str, Any] = {"sdf:jsonPointer": json_pointer}

    return wot_action


def map_property_qualities(
    sdf_model: Dict,
    thing_model: Dict,
    sdf_property: Dict,
    affordance_key: str,
    json_pointer: str,
):
    initialize_object_field(thing_model, "properties")

    wot_property = create_wot_affordance(json_pointer)
    collect_sdf_required(thing_model, sdf_property)
    collect_mapping(thing_model, json_pointer, "properties", affordance_key)

    map_data_qualities(sdf_model, sdf_property, wot_property, is_property=True)

    thing_model["properties"][affordance_key] = wot_property


# TODO: Find a better name for this function
def map_sdf_data_qualities(
    sdf_model: Dict,
    thing_model: Dict,
    sdf_property: Dict,
    affordance_key: str,
    json_pointer: str,
):
    initialize_object_field(thing_model, "schemaDefinitions")

    wot_schema_definition = create_wot_affordance(json_pointer)
    collect_sdf_required(thing_model, sdf_property)
    collect_mapping(thing_model, json_pointer, "schemaDefinitions", affordance_key)

    map_data_qualities(
        sdf_model, sdf_property, wot_schema_definition, is_property=False
    )

    thing_model["schemaDefinitions"][affordance_key] = wot_schema_definition


def map_sdf_data(
    sdf_model: Dict,
    sdf_definition: Dict,
    thing_model: Dict,
    prefix_list: List[str],
    json_pointer_prefix: str,
    suffix="",
):
    for key, sdf_property in sdf_definition.get("sdfData", {}).items():
        name_list = prefix_list + [key]
        if suffix:
            name_list.append(suffix)
        affordance_key = "_".join(name_list)
        json_pointer = get_json_pointer(json_pointer_prefix, "sdfData", key)
        map_sdf_data_qualities(
            sdf_model, thing_model, sdf_property, affordance_key, json_pointer
        )


def map_sdf_action(
    sdf_model: Dict,
    sdf_definition: Dict,
    thing_model: Dict,
    prefix_list: List[str],
    json_pointer_prefix: str,
):
    for key, sdf_action in sdf_definition.get("sdfAction", {}).items():
        json_pointer = get_json_pointer(json_pointer_prefix, "sdfAction", key)
        map_action_qualities(
            sdf_model, thing_model, sdf_action, prefix_list + [key], json_pointer
        )


def map_object_qualities(
    sdf_model: Dict,
    sdf_definition: Dict,
    thing_model: Dict,
    prefix_list: List[str],
    json_pointer_prefix: str,
):
    for key, sdf_object in sdf_definition.get("sdfObject", {}).items():
        collect_sdf_required(thing_model, sdf_object)
        sdf_object = resolve_sdf_ref(sdf_model, sdf_object, None, [])
        json_pointer = get_json_pointer(json_pointer_prefix, "sdfObject", key)
        map_sdf_data(
            sdf_model, sdf_object, thing_model, prefix_list + [key], json_pointer
        )
        map_sdf_action(
            sdf_model, sdf_object, thing_model, prefix_list + [key], json_pointer
        )
        map_sdf_property(
            sdf_model, sdf_object, thing_model, prefix_list + [key], json_pointer
        )
        map_sdf_event(
            sdf_model, sdf_object, thing_model, prefix_list + [key], json_pointer
        )


def map_thing_qualities(
    sdf_model: Dict,
    sdf_definition: Dict,
    thing_model: Dict,
    prefix_list: List[str],
    json_pointer_prefix: str,
    sdf_product=False,
):
    quality_name = "sdfThing"
    if sdf_product:
        quality_name = "sdfProduct"
    for key, sdf_thing in sdf_definition.get(quality_name, {}).items():
        collect_sdf_required(thing_model, sdf_thing)
        sdf_thing = resolve_sdf_ref(sdf_model, sdf_thing, None, [])
        json_pointer = get_json_pointer(json_pointer_prefix, quality_name, key)
        map_thing_qualities(
            sdf_model, sdf_thing, thing_model, prefix_list + [key], json_pointer
        )
        map_object_qualities(
            sdf_model, sdf_thing, thing_model, prefix_list + [key], json_pointer
        )


def get_json_pointer(json_pointer_prefix: str, infix: str, key: str):
    pointer_prefix = f"{json_pointer_prefix}/{infix}/{key}"
    return pointer_prefix


def map_sdf_property(
    sdf_model: Dict,
    sdf_definition: Dict,
    thing_model: Dict,
    prefix_list: List[str],
    json_pointer_prefix: str,
):
    for key, sdf_property in sdf_definition.get("sdfProperty", {}).items():
        affordance_key = "_".join(prefix_list + [key])
        json_pointer = get_json_pointer(json_pointer_prefix, "sdfProperty", key)
        map_property_qualities(
            sdf_model, thing_model, sdf_property, affordance_key, json_pointer
        )


def map_event_qualities(
    sdf_model: Dict,
    thing_model: Dict,
    sdf_event: Dict,
    prefix_list: List[str],
    json_pointer: str,
):
    initialize_object_field(thing_model, "events")
    affordance_key = "_".join(prefix_list)

    wot_event = create_wot_affordance(json_pointer)
    collect_sdf_required(thing_model, sdf_event)
    collect_mapping(thing_model, json_pointer, "events", affordance_key)
    sdf_event = resolve_sdf_ref(sdf_model, sdf_event, None, [])

    map_common_qualities(sdf_event, wot_event)

    if "sdfOutputData" in sdf_event:
        wot_event["data"] = {}
        map_data_qualities(sdf_model, sdf_event["sdfOutputData"], wot_event["data"])

    map_sdf_data(
        sdf_model, sdf_event, thing_model, prefix_list, json_pointer, suffix="event"
    )

    thing_model["events"][affordance_key] = wot_event


def collect_sdf_required(thing_model: Dict, sdf_definition: Dict):
    initialize_list_field(thing_model, "tm:required")
    thing_model["tm:required"].extend(sdf_definition.get("sdfRequired", []))


def collect_mapping(thing_model, json_pointer, definition_type, definition_key):
    thing_model["mappings"][json_pointer] = f"#/{definition_type}/{definition_key}"


def map_sdf_event(
    sdf_model: Dict,
    sdf_definition: Dict,
    thing_model: Dict,
    prefix_list: List[str],
    json_pointer_prefix: str,
):
    for key, sdf_event in sdf_definition.get("sdfEvent", {}).items():
        json_pointer = get_json_pointer(json_pointer_prefix, "sdfEvent", key)
        map_event_qualities(
            sdf_model, thing_model, sdf_event, prefix_list + [key], json_pointer
        )


def map_sdf_required(thing_model: Dict):
    required_affordances = []
    for pointer in thing_model.get("tm:required", []):
        if pointer in thing_model["mappings"]:
            required_affordances.append(thing_model["mappings"][pointer])
    thing_model["tm:required"] = required_affordances
    if not thing_model["tm:required"]:
        del thing_model["tm:required"]


def map_sdf_ref(thing_model: Dict, current_definition: Dict):
    if "tm:ref" in current_definition:
        old_pointer = current_definition["tm:ref"]
        current_definition["tm:ref"] = thing_model["mappings"][old_pointer]

    for value in current_definition.values():
        if isinstance(value, dict):
            map_sdf_ref(thing_model, value)


def convert_sdf_to_wot_tm(sdf_model: Dict) -> Dict:

    thing_model: Dict = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": "tm:ThingModel",
        "mappings": {},
    }

    map_infoblock(sdf_model, thing_model)
    map_namespace(sdf_model, thing_model)
    map_default_namespace(sdf_model, thing_model)

    map_thing_qualities(sdf_model, sdf_model, thing_model, [], "#", sdf_product=True)
    map_thing_qualities(sdf_model, sdf_model, thing_model, [], "#")
    map_object_qualities(sdf_model, sdf_model, thing_model, [], "#")

    map_sdf_data(sdf_model, sdf_model, thing_model, [], "#")
    map_sdf_action(sdf_model, sdf_model, thing_model, [], "#")
    map_sdf_property(sdf_model, sdf_model, thing_model, [], "#")
    map_sdf_event(sdf_model, sdf_model, thing_model, [], "#")

    map_sdf_required(thing_model)
    map_sdf_ref(thing_model, thing_model)
    del thing_model["mappings"]

    return thing_model
