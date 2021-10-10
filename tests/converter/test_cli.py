import json
from sdf_wot_converter import (
    _parse_arguments,
    _resolve_tm_input,
    convert_sdf_to_wot_tm_from_path,
    convert_wot_tm_to_sdf_from_path,
    convert_wot_tm_to_sdf_from_paths,
    convert_wot_tm_to_td_from_paths,
    convert_wot_tm_to_wot_td_from_path,
    convert_wot_td_to_wot_tm_from_path,
    convert_sdf_to_wot_tm_from_json,
    convert_wot_tm_to_sdf_from_json,
    convert_wot_tm_to_wot_td_from_json,
    convert_wot_td_to_wot_tm_from_json,
    get_origin_url,
)
import os


def test_parse_arguments():
    args1 = ["--from-sdf", "foo", "--to-tm", "bar"]
    parsed_args1 = _parse_arguments(args1)
    assert parsed_args1.from_sdf == "foo" and parsed_args1.to_tm == "bar"

    args2 = ["--from-tm", "foo", "--to-sdf", "bar"]
    parsed_args2 = _parse_arguments(args2)
    assert parsed_args2.from_tm == ["foo"] and parsed_args2.to_sdf == "bar"


def make_test_output_dir():
    try:
        os.mkdir("test_output")
    except FileExistsError:
        pass


def test_resolve_tm_input():
    expected_result = {
        "@context": "https://www.w3.org/2019/wot/td/v1",
        "@type": "tm:ThingModel",
        "actions": {
            "toggle": {
                "@type": "saref:ToggleCommand",
                "forms": [{"href": "https://mylamp.example.com/toggle"}],
            }
        },
        "events": {
            "overheating": {
                "data": {"type": "string"},
                "forms": [
                    {"href": "https://mylamp.example.com/oh", "subprotocol": "longpoll"}
                ],
            }
        },
        "id": "urn:dev:ops:32473-WoTLamp-1234",
        "properties": {
            "status": {
                "@type": "saref:OnOffState",
                "forms": [{"href": "https://mylamp.example.com/status"}],
                "type": "string",
            }
        },
        "security": "basic_sc",
        "securityDefinitions": {"basic_sc": {"in": "header", "scheme": "basic"}},
        "title": "MyLampThing",
        "base": "BASE_ADDRESS",
    }

    result = _resolve_tm_input(
        [
            "examples/wot/example-with-placeholders.tm.jsonld",
            "examples/wot/example-with-tm-extends.tm.jsonld",
        ],
        True,
    )
    assert result == expected_result


def test_resolve_tm_input_without_extends_resolution():
    expected_result = {
        "@context": "https://www.w3.org/2019/wot/td/v1",
        "@type": "tm:ThingModel",
        "id": "urn:dev:ops:32473-WoTLamp-1234",
        "security": "basic_sc",
        "securityDefinitions": {"basic_sc": {"in": "header", "scheme": "basic"}},
        "links": [
            {
                "href": "https://raw.githubusercontent.com/JKRhb/sdf-wot-converter-py/main/examples/wot/example-with-bindings.tm.jsonld",
                "rel": "tm:extends",
            }
        ],
        "title": "MyLampThing",
        "base": "BASE_ADDRESS",
    }

    result = _resolve_tm_input(
        [
            "examples/wot/example-with-placeholders.tm.jsonld",
            "examples/wot/example-with-tm-extends.tm.jsonld",
        ],
        False,
    )
    assert result == expected_result


def test_sdf_example_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_sdf_to_wot_tm_from_path(
        "examples/sdf/example.sdf.json", "test_output/blah.tm.jsonld"
    )


def test_wot_example_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_wot_tm_to_sdf_from_path(
        "examples/wot/example.tm.jsonld", "test_output/blah.sdf.json"
    )


def test_multiple_tms_to_sdf_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_wot_tm_to_sdf_from_paths(
        [
            "examples/wot/example.tm.jsonld",
            "examples/wot/example-with-tm-extends.tm.jsonld",
        ],
        "test_output/multipleconvertedtms.sdf.json",
    )


def test_multiple_tms_to_td_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_wot_tm_to_td_from_paths(
        [
            "examples/wot/example.tm.jsonld",
            "examples/wot/example-with-tm-extends.tm.jsonld",
        ],
        "test_output/multipleconvertedtms.td.json",
    )


def test_wot_tm_td_example_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_wot_tm_to_wot_td_from_path(
        "examples/wot/example-with-bindings.tm.jsonld", "test_output/blah.td.jsonld"
    )


def test_wot_tm_td_placeholder_example_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_wot_tm_to_wot_td_from_path(
        "examples/wot/example-with-placeholders.tm.jsonld",
        "test_output/blah_placeholders.td.jsonld",
        placeholder_map_path="examples/wot/placeholders.json",
    )


def test_wot_td_tm_example_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_wot_td_to_wot_tm_from_path(
        "examples/wot/example.td.jsonld", "test_output/from_td.tm.jsonld"
    )


def test_sdf_json_conversion():
    input = {}

    expected_result = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
    }

    result = json.loads(convert_sdf_to_wot_tm_from_json(json.dumps(input)))

    assert result == expected_result


def test_wot_json_conversion():
    input = {
        "@context": "http://www.w3.org/ns/td",
        "@type": "tm:ThingModel",
    }

    expected_result = {}

    result = json.loads(convert_wot_tm_to_sdf_from_json(json.dumps(input)))

    assert result == expected_result


def test_wot_tm_td_json_conversion():
    input = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": "tm:ThingModel",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": "Thing",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    result = json.loads(convert_wot_tm_to_wot_td_from_json(json.dumps(input)))

    assert result == expected_result


def test_wot_tm_td_json_conversion_with_meta_data():
    input = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": "tm:ThingModel",
    }

    meta_data = {
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": "Thing",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    result = json.loads(
        convert_wot_tm_to_wot_td_from_json(
            json.dumps(input), meta_data_json=json.dumps(meta_data)
        )
    )

    assert result == expected_result


def test_wot_td_tm_json_conversion():

    input = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": "Thing",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": "tm:ThingModel",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    result = json.loads(convert_wot_td_to_wot_tm_from_json(json.dumps(input)))

    assert result == expected_result


def test_get_origin_url():
    assert get_origin_url(None, None) == None
    assert get_origin_url("http://example.com", None) == "http://example.com"
    assert get_origin_url("https://example.com", None) == "https://example.com"
    assert get_origin_url(None, "http://example.com") == "http://example.com"
    assert get_origin_url("http://hi.com", "http://example.com") == "http://example.com"
    assert get_origin_url("this/is/a/file/path", None) == None
