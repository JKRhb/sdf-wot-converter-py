from typing import (
    Any,
    Dict,
    List,
    Optional,
)
from jsonpointer import resolve_pointer
import json_merge_patch
import urllib.request

from .common.jsonschema import map_common_json_schema_fields
from .utility import (
    initialize_list_field,
    initialize_object_field,
    map_common_field,
    map_field,
    negate,
)
import json
import validators


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


def map_namespace(
    sdf_model: Dict,
    thing_model: Dict,
    suppress_roundtripping: bool,
    mapped_fields: List[str],
):
    namespaces = sdf_model.get("namespace", {}).copy()
    mapped_fields.append("namespace")
    if not suppress_roundtripping:
        namespaces["sdf"] = "https://example.com/sdf"
    if len(namespaces) > 0:
        thing_model["@context"].append(namespaces)


def map_default_namespace(
    sdf_model: Dict,
    thing_model: Dict,
    suppress_roundtripping: bool,
    mapped_fields: List[str],
):
    if suppress_roundtripping:
        return

    map_field(
        sdf_model,
        thing_model,
        "defaultNamespace",
        "sdf:defaultNamespace",
        mapped_fields=mapped_fields,
    )


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


def map_license(infoblock: Dict, thing_model: Dict, suppress_roundtripping: bool):
    license = infoblock.get("license")

    if license is not None:
        valid_url = validators.url(license)

        if valid_url:
            add_link(thing_model, license, None, "license", None, None)
        elif not suppress_roundtripping:
            thing_model["sdf:license"] = license


def map_version(infoblock: Dict, thing_model: Dict, set_instance_version: bool):
    version = infoblock.get("version")
    if version is not None:
        tm_version = {"model": version}

        if set_instance_version:
            tm_version["instance"] = version

        thing_model["version"] = tm_version


def map_infoblock(
    sdf_model: Dict,
    thing_model: Dict,
    set_instance_version: bool,
    suppress_roundtripping: bool,
    mapped_fields: List[str],
):
    infoblock = sdf_model.get("info")
    if infoblock:
        mapped_fields.append("info")
        map_title(thing_model, infoblock, suppress_roundtripping)
        map_copyright(thing_model, infoblock, suppress_roundtripping)
        map_license(infoblock, thing_model, suppress_roundtripping)
        map_version(infoblock, thing_model, set_instance_version)


def map_copyright(thing_model, infoblock, suppress_roundtripping: bool):
    if suppress_roundtripping:
        return

    map_field(infoblock, thing_model, "copyright", "sdf:copyright")


def map_title(thing_model, infoblock, suppress_roundtripping: bool):
    if suppress_roundtripping:
        return

    map_field(infoblock, thing_model, "title", "sdf:title")


def map_common_qualities(
    sdf_definition: Dict,
    wot_definition: Dict,
    suppress_roundtripping,
    mapped_fields: List[str],
):
    map_label(sdf_definition, wot_definition, mapped_fields)
    map_description(sdf_definition, wot_definition, mapped_fields)
    map_comment(sdf_definition, wot_definition, suppress_roundtripping, mapped_fields)
    copy_sdf_ref(sdf_definition, wot_definition, mapped_fields)


def copy_sdf_ref(sdf_definition, wot_definition, mapped_fields: List[str]):
    sdf_ref = sdf_definition.get("sdfRef")
    if sdf_ref is not None:
        mapped_fields.append("sdfRef")
        if sdf_ref.startswith("#"):
            wot_definition["tm:ref"] = sdf_definition["sdfRef"]


def map_comment(
    sdf_definition,
    wot_definition,
    suppress_roundtripping: bool,
    mapped_fields: List[str],
):
    if suppress_roundtripping:
        return

    map_field(
        sdf_definition,
        wot_definition,
        "$comment",
        "sdf:$comment",
        mapped_fields=mapped_fields,
    )


def map_description(sdf_definition, wot_definition, mapped_fields: List[str]):
    map_common_field(
        sdf_definition, wot_definition, "description", mapped_fields=mapped_fields
    )


def map_label(sdf_definition: Dict, wot_definition: Dict, mapped_fields: List[str]):
    map_field(
        sdf_definition, wot_definition, "label", "title", mapped_fields=mapped_fields
    )


def map_sdf_choice(
    sdf_model: Dict,
    data_qualities: Dict,
    data_schema: Dict,
    suppress_roundtripping: bool,
    mapped_fields: List[str],
):
    if "sdfChoice" in data_qualities:
        mapped_fields.append("sdfChoice")
        initialize_list_field(data_schema, "enum")
        for choice_name, choice in data_qualities["sdfChoice"].items():
            mapped_choice = {}
            if not suppress_roundtripping:
                mapped_choice["sdf:choiceName"] = choice_name
            mapped_choice_fields: List[str] = []
            map_data_qualities(
                sdf_model,
                choice,
                mapped_choice,
                suppress_roundtripping,
                mapped_choice_fields,
            )
            data_schema["enum"].append(mapped_choice)


def map_data_qualities(
    sdf_model: Dict,
    data_qualities: Dict,
    data_schema: Dict,
    suppress_roundtripping: bool,
    mapped_fields: List[str],
    is_property=False,
    is_choice=False,
):
    data_qualities = resolve_sdf_ref(sdf_model, data_qualities, None, [])

    map_common_qualities(
        data_qualities, data_schema, suppress_roundtripping, mapped_fields
    )

    map_common_json_schema_fields(
        data_qualities, data_schema, mapped_fields=mapped_fields
    )
    map_enum(data_qualities, data_schema, mapped_fields)

    # TODO: Revisit the mapping of these two fields
    map_nullable(data_qualities, data_schema, suppress_roundtripping, mapped_fields)
    map_sdf_type(data_qualities, data_schema, suppress_roundtripping, mapped_fields)

    map_sdf_choice(
        sdf_model, data_qualities, data_schema, suppress_roundtripping, mapped_fields
    )
    map_content_format(data_qualities, data_schema, mapped_fields)

    map_items(
        sdf_model, data_qualities, data_schema, suppress_roundtripping, mapped_fields
    )

    map_properties(
        sdf_model, data_qualities, data_schema, suppress_roundtripping, mapped_fields
    )

    if is_property:
        map_observable(data_qualities, data_schema, mapped_fields)
        map_writable(data_qualities, data_schema, mapped_fields)
        map_readable(data_qualities, data_schema, mapped_fields)

    map_additional_fields(data_schema, data_qualities, mapped_fields)


def map_writable(sdf_property, wot_property, mapped_fields):
    map_field(
        sdf_property,
        wot_property,
        "writable",
        "readOnly",
        conversion_function=negate,
        mapped_fields=mapped_fields,
    )


def map_readable(sdf_property, wot_property, mapped_fields):
    map_field(
        sdf_property,
        wot_property,
        "readable",
        "writeOnly",
        conversion_function=negate,
        mapped_fields=mapped_fields,
    )


def map_properties(
    sdf_model, data_qualities, data_schema, suppress_roundtripping: bool, mapped_fields
):
    properties = data_qualities.get("properties")

    if properties is None:
        return

    mapped_fields.append("properties")

    for key, property in properties.items():
        initialize_object_field(data_schema, "properties")
        data_schema["properties"][key] = {}
        mapped_property_fields: List[str] = []
        map_data_qualities(
            sdf_model,
            property,
            data_schema["properties"][key],
            suppress_roundtripping,
            mapped_property_fields,
        )


def map_items(
    sdf_model, data_qualities, data_schema, suppress_roundtripping: bool, mapped_fields
):
    if "items" in data_qualities:
        mapped_fields.append("items")
        data_schema["items"] = {}
        mapped_item_fields: List[str] = []
        map_data_qualities(
            sdf_model,
            data_qualities["items"],
            data_schema["items"],
            suppress_roundtripping,
            mapped_item_fields,
        )


def map_observable(wot_property: Dict, sdf_property: Dict, mapped_fields):
    mapped_fields.append("observable")
    sdf_property["observable"] = wot_property.get("observable", True)


def map_sdf_type(
    data_qualities, data_schema, suppress_roundtripping: bool, mapped_fields
):
    if suppress_roundtripping:
        return

    map_field(
        data_qualities,
        data_schema,
        "sdfType",
        "sdf:sdfType",
        mapped_fields=mapped_fields,
    )


def map_nullable(
    data_qualities, data_schema, suppress_roundtripping: bool, mapped_fields
):
    if suppress_roundtripping:
        return

    map_field(
        data_qualities,
        data_schema,
        "nullable",
        "sdf:nullable",
        mapped_fields=mapped_fields,
    )


def map_content_format(data_qualities, data_schema, mapped_fields):
    map_field(
        data_qualities,
        data_schema,
        "contentFormat",
        "contentMediaType",
        mapped_fields=mapped_fields,
    )


def map_enum(data_qualities, data_schema, mapped_fields):
    map_common_field(data_qualities, data_schema, "enum", mapped_fields=mapped_fields)


def map_action_qualities(
    sdf_model: Dict,
    thing_model: Dict,
    sdf_action: Dict,
    prefix_list: List[str],
    json_pointer: str,
    suppress_roundtripping: bool,
):
    initialize_object_field(thing_model, "actions")
    affordance_key = "_".join(prefix_list)

    wot_action: Dict[str, Any] = {}
    mapped_fields: List[str] = []
    collect_sdf_required(thing_model, sdf_action, mapped_fields)
    collect_mapping(thing_model, json_pointer, "actions", affordance_key)
    sdf_action = resolve_sdf_ref(sdf_model, sdf_action, None, [])

    map_common_qualities(sdf_action, wot_action, suppress_roundtripping, mapped_fields)

    data_map_pairs = [("sdfInputData", "input"), ("sdfOutputData", "output")]

    for sdf_field, wot_field in data_map_pairs:
        if sdf_field in sdf_action:
            mapped_fields.append(sdf_field)
            wot_action[wot_field] = {}
            mapped_data_quality_fields: List[str] = []
            map_data_qualities(
                sdf_model,
                sdf_action[sdf_field],
                wot_action[wot_field],
                suppress_roundtripping,
                mapped_data_quality_fields,
            )

    map_sdf_data(
        sdf_model,
        sdf_action,
        thing_model,
        prefix_list,
        json_pointer,
        suppress_roundtripping,
        mapped_fields,
        suffix="action",
    )

    map_additional_fields(wot_action, sdf_action, mapped_fields)

    thing_model["actions"][affordance_key] = wot_action


def map_property_qualities(
    sdf_model: Dict,
    thing_model: Dict,
    sdf_property: Dict,
    affordance_key: str,
    json_pointer: str,
    suppress_roundtripping: bool,
):
    initialize_object_field(thing_model, "properties")

    wot_property: Dict[str, Any] = {}
    mapped_fields: List[str] = []
    collect_sdf_required(thing_model, sdf_property, mapped_fields)
    collect_mapping(thing_model, json_pointer, "properties", affordance_key)

    map_data_qualities(
        sdf_model,
        sdf_property,
        wot_property,
        suppress_roundtripping,
        mapped_fields,
        is_property=True,
    )

    map_additional_fields(wot_property, sdf_property, mapped_fields)

    thing_model["properties"][affordance_key] = wot_property


# TODO: Find a better name for this function
def map_sdf_data_qualities(
    sdf_model: Dict,
    thing_model: Dict,
    sdf_data: Dict,
    affordance_key: str,
    json_pointer: str,
    suppress_roundtripping: bool,
):
    initialize_object_field(thing_model, "schemaDefinitions")

    wot_schema_definition: Dict[str, Any] = {}
    mapped_fields: List[str] = []
    collect_sdf_required(thing_model, sdf_data, mapped_fields)
    collect_mapping(thing_model, json_pointer, "schemaDefinitions", affordance_key)

    map_data_qualities(
        sdf_model,
        sdf_data,
        wot_schema_definition,
        suppress_roundtripping,
        mapped_fields,
        is_property=False,
    )

    map_common_qualities(
        sdf_data, wot_schema_definition, suppress_roundtripping, mapped_fields
    )

    map_additional_fields(wot_schema_definition, sdf_data, mapped_fields)

    thing_model["schemaDefinitions"][affordance_key] = wot_schema_definition


def map_sdf_data(
    sdf_model: Dict,
    sdf_definition: Dict,
    thing_model: Dict,
    prefix_list: List[str],
    json_pointer_prefix: str,
    suppress_roundtripping: bool,
    mapped_fields: List[str],
    suffix="",
):
    sdf_data = sdf_definition.get("sdfData")

    if sdf_data is None:
        return

    mapped_fields.append("sdfData")

    for key, sdf_property in sdf_data.items():
        name_list = prefix_list + [key]
        if suffix:
            name_list.append(suffix)
        affordance_key = "_".join(name_list)
        json_pointer = get_json_pointer(json_pointer_prefix, "sdfData", key)
        map_sdf_data_qualities(
            sdf_model,
            thing_model,
            sdf_property,
            affordance_key,
            json_pointer,
            suppress_roundtripping,
        )


def map_sdf_action(
    sdf_model: Dict,
    sdf_definition: Dict,
    thing_model: Dict,
    prefix_list: List[str],
    json_pointer_prefix: str,
    suppress_roundtripping: bool,
    mapped_fields: List[str],
):
    sdf_actions = sdf_definition.get("sdfAction")

    if sdf_actions is None:
        return

    mapped_fields.append("sdfAction")

    for key, sdf_action in sdf_actions.items():
        json_pointer = get_json_pointer(json_pointer_prefix, "sdfAction", key)
        map_action_qualities(
            sdf_model,
            thing_model,
            sdf_action,
            prefix_list + [key],
            json_pointer,
            suppress_roundtripping,
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
    suppress_roundtripping: bool,
    mapped_fields: List[str],
):
    sdf_properties = sdf_definition.get("sdfProperty")

    if sdf_properties is None:
        return

    mapped_fields.append("sdfProperty")

    for key, sdf_property in sdf_properties.items():
        affordance_key = "_".join(prefix_list + [key])
        json_pointer = get_json_pointer(json_pointer_prefix, "sdfProperty", key)
        map_property_qualities(
            sdf_model,
            thing_model,
            sdf_property,
            affordance_key,
            json_pointer,
            suppress_roundtripping,
        )


def map_event_qualities(
    sdf_model: Dict,
    thing_model: Dict,
    sdf_event: Dict,
    prefix_list: List[str],
    json_pointer: str,
    suppress_roundtripping: bool,
):
    initialize_object_field(thing_model, "events")
    affordance_key = "_".join(prefix_list)

    wot_event: Dict[str, Any] = {}
    mapped_fields: List[str] = []
    collect_sdf_required(thing_model, sdf_event, mapped_fields)
    collect_mapping(thing_model, json_pointer, "events", affordance_key)
    sdf_event = resolve_sdf_ref(sdf_model, sdf_event, None, [])

    map_common_qualities(sdf_event, wot_event, suppress_roundtripping, mapped_fields)

    if "sdfOutputData" in sdf_event:
        mapped_fields.append("sdfOutputData")
        wot_event["data"] = {}
        mapped_output_data_fields: List[str] = []
        map_data_qualities(
            sdf_model,
            sdf_event["sdfOutputData"],
            wot_event["data"],
            suppress_roundtripping,
            mapped_output_data_fields,
        )

    map_sdf_data(
        sdf_model,
        sdf_event,
        thing_model,
        prefix_list,
        json_pointer,
        suppress_roundtripping,
        mapped_fields,
        suffix="event",
    )

    map_additional_fields(wot_event, sdf_event, mapped_fields)

    thing_model["events"][affordance_key] = wot_event


def collect_sdf_required(
    thing_model: Dict, sdf_definition: Dict, mapped_fields: List[str]
):
    mapped_fields.append("sdfRequired")
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
    suppress_roundtripping: bool,
    mapped_fields: List[str],
):
    sdf_events = sdf_definition.get("sdfEvent")

    if sdf_events is None:
        return

    mapped_fields.append("sdfEvent")

    for key, sdf_event in sdf_events.items():
        json_pointer = get_json_pointer(json_pointer_prefix, "sdfEvent", key)
        map_event_qualities(
            sdf_model,
            thing_model,
            sdf_event,
            prefix_list + [key],
            json_pointer,
            suppress_roundtripping,
        )


def map_sdf_required(thing_model: Dict, mapped_fields: List[str]):
    tm_required = thing_model.get("tm:required")
    mapped_fields.extend(["tm:required", "mappings"])

    if tm_required is None:
        return

    thing_model["tm:required"] = [
        thing_model["mappings"][pointer] for pointer in tm_required
    ]

    if len(thing_model["tm:required"]) == 0:
        del thing_model["tm:required"]


def map_sdf_ref(thing_model: Dict, current_definition: Dict, mapped_fields=None):
    if "tm:ref" in current_definition:
        if mapped_fields is not None:
            mapped_fields.append("tm:ref")
        old_pointer = current_definition["tm:ref"]
        current_definition["tm:ref"] = thing_model["mappings"][old_pointer]

    for value in current_definition.values():
        if isinstance(value, dict):
            map_sdf_ref(thing_model, value)


def add_origin_link(thing_model: Dict, origin_url: str):
    if origin_url:
        origin_link = {
            "href": origin_url,
            "rel": "alternate",  # TODO: Which kind of link relation should be used?
        }
        if "links" in thing_model:
            thing_model["links"].append(origin_link)
        else:
            thing_model["links"] = [origin_link]


def create_basic_thing_model():
    return {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "mappings": {},
    }


def map_sdf_objects(
    thing_models: Dict[str, Dict],
    sdf_model: Dict,
    sdf_definition: Dict,
    pointer_prefix: str,
    parent=None,
    origin_url=None,
    parent_mapped_fields=None,
    set_instance_version=False,
    suppress_roundtripping=False,
) -> None:
    if parent_mapped_fields is not None:
        parent_mapped_fields.append("sdfObject")

    for object_key, sdf_object in sdf_definition.get("sdfObject", {}).items():
        json_pointer = f"{pointer_prefix}/sdfObject/{object_key}"

        mapped_fields: List[str] = []

        thing_model: Dict = create_basic_thing_model()
        if not suppress_roundtripping:
            thing_model["sdf:objectKey"] = object_key
        collect_sdf_required(thing_model, sdf_object, mapped_fields)
        # collect_mapping(thing_model, json_pointer, "events", affordance_key)
        map_infoblock(
            sdf_model,
            thing_model,
            set_instance_version,
            suppress_roundtripping,
            mapped_fields,
        )
        map_namespace(sdf_model, thing_model, suppress_roundtripping, mapped_fields)
        map_default_namespace(
            sdf_model, thing_model, suppress_roundtripping, mapped_fields
        )
        map_common_qualities(
            sdf_object, thing_model, suppress_roundtripping, mapped_fields
        )
        map_sdf_data(
            sdf_model,
            sdf_object,
            thing_model,
            [],
            json_pointer,
            suppress_roundtripping,
            mapped_fields,
        )
        map_sdf_action(
            sdf_model,
            sdf_object,
            thing_model,
            [],
            json_pointer,
            suppress_roundtripping,
            mapped_fields,
        )
        map_sdf_property(
            sdf_model,
            sdf_object,
            thing_model,
            [],
            json_pointer,
            suppress_roundtripping,
            mapped_fields,
        )
        map_sdf_event(
            sdf_model,
            sdf_object,
            thing_model,
            [],
            json_pointer,
            suppress_roundtripping,
            mapped_fields,
        )

        map_sdf_required(thing_model, mapped_fields)
        map_sdf_ref(thing_model, thing_model, mapped_fields=mapped_fields)
        del thing_model["mappings"]

        map_additional_fields(thing_model, sdf_object, mapped_fields)

        add_origin_link(thing_model, origin_url)
        add_link_to_parent(parent, object_key)

        thing_models[object_key] = thing_model


def map_additional_fields(
    wot_definition: dict, sdf_definition: dict, mapped_fields: List[str]
):
    for key, value in sdf_definition.items():
        if key in mapped_fields:
            continue

        wot_definition[key] = value


def add_link_to_parent(parent: dict, json_pointer: str):
    if parent:
        parent_link = {
            "href": f"#/{json_pointer}",
            "rel": "tm:submodel",  # TODO: Which kind of link relation should be used?
        }
        if "links" in parent:
            parent["links"].append(parent_link)
        else:
            parent["links"] = [parent_link]


def map_sdf_things(
    thing_models: Dict[str, Dict],
    sdf_model: Dict,
    sdf_definition: Dict,
    current_prefix: str,
    origin_url=None,
    parent=None,
    parent_mapped_fields=None,
    set_instance_version=False,
    suppress_roundtripping=False,
) -> None:
    if parent_mapped_fields is not None:
        parent_mapped_fields.append("sdfThing")

    for thing_key, sdf_thing in sdf_definition.get("sdfThing", {}).items():
        thing_prefix = f"{current_prefix}/sdfThing/{thing_key}"

        mapped_fields: List[str] = []

        thing_model: Dict = create_basic_thing_model()
        if not suppress_roundtripping:
            thing_model["sdf:thingKey"] = thing_key
        collect_sdf_required(thing_model, sdf_thing, mapped_fields)
        map_infoblock(
            sdf_model,
            thing_model,
            set_instance_version,
            suppress_roundtripping,
            mapped_fields,
        )
        map_namespace(sdf_model, thing_model, suppress_roundtripping, mapped_fields)
        map_default_namespace(
            sdf_model, thing_model, suppress_roundtripping, mapped_fields
        )
        map_common_qualities(
            sdf_thing, thing_model, suppress_roundtripping, mapped_fields
        )
        map_sdf_data(
            sdf_model,
            sdf_thing,
            thing_model,
            [],
            thing_prefix,
            suppress_roundtripping,
            mapped_fields,
        )
        map_sdf_action(
            sdf_model,
            sdf_thing,
            thing_model,
            [],
            thing_prefix,
            suppress_roundtripping,
            mapped_fields,
        )
        map_sdf_property(
            sdf_model,
            sdf_thing,
            thing_model,
            [],
            thing_prefix,
            suppress_roundtripping,
            mapped_fields,
        )
        map_sdf_event(
            sdf_model,
            sdf_thing,
            thing_model,
            [],
            thing_prefix,
            suppress_roundtripping,
            mapped_fields,
        )

        map_sdf_required(thing_model, mapped_fields)
        map_sdf_ref(thing_model, thing_model, mapped_fields)
        del thing_model["mappings"]

        add_origin_link(thing_model, origin_url)
        add_link_to_parent(parent, thing_key)

        thing_models[thing_key] = thing_model

        map_sdf_things(
            thing_models,
            sdf_model,
            sdf_thing,
            thing_prefix,
            parent=thing_model,
            origin_url=origin_url,
            parent_mapped_fields=mapped_fields,
            suppress_roundtripping=suppress_roundtripping,
        )
        map_sdf_objects(
            thing_models,
            sdf_model,
            sdf_thing,
            thing_prefix,
            parent=thing_model,
            origin_url=origin_url,
            parent_mapped_fields=mapped_fields,
            suppress_roundtripping=suppress_roundtripping,
        )

        map_additional_fields(thing_model, sdf_thing, mapped_fields)


def _apply_mapping_file(sdf_model: Dict, sdf_mapping_file: Dict):
    # TODO: Add mapping file validation

    for pointer, value in sdf_mapping_file["map"].items():
        original = resolve_pointer(sdf_model, pointer[1:])

        json_merge_patch.merge(original, value)


def consolidate_sdf_model(sdf_model: Dict, sdf_mapping_files: List[Dict]):
    for sdf_mapping_file in sdf_mapping_files:
        _apply_mapping_file(sdf_model, sdf_mapping_file)


def convert_sdf_to_wot_tm(
    sdf_model: Dict,
    sdf_mapping_files: Optional[List[Dict]] = None,
    origin_url=None,
    set_instance_version=False,
    suppress_roundtripping=False,
) -> Dict[str, Dict]:

    if sdf_mapping_files is not None:
        consolidate_sdf_model(sdf_model, sdf_mapping_files)

    thing_models: Dict[str, Dict] = {}
    map_sdf_objects(
        thing_models,
        sdf_model,
        sdf_model,
        "#",
        origin_url=origin_url,
        set_instance_version=set_instance_version,
        suppress_roundtripping=suppress_roundtripping,
    )
    map_sdf_things(
        thing_models,
        sdf_model,
        sdf_model,
        "#",
        origin_url=origin_url,
        set_instance_version=set_instance_version,
        suppress_roundtripping=suppress_roundtripping,
    )

    # TODO: Find a better solution for this
    if len(thing_models) == 1:
        thing_models = list(thing_models.values())[0]

    return thing_models
