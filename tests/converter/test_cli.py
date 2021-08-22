import json
from sdf_wot_converter import (
    _parse_arguments,
    convert_sdf_to_wot_tm_from_path,
    convert_wot_tm_to_sdf_from_path,
    convert_wot_tm_to_wot_td_from_path,
    convert_sdf_to_wot_tm_from_json,
    convert_wot_tm_to_sdf_from_json,
    convert_wot_tm_to_wot_td_from_json,
)
import os


def test_parse_arguments():
    args1 = ["--from-sdf", "foo", "--to-tm", "bar"]
    parsed_args1 = _parse_arguments(args1)
    assert parsed_args1.from_sdf == "foo" and parsed_args1.to_tm == "bar"

    args2 = ["--from-tm", "foo", "--to-sdf", "bar"]
    parsed_args2 = _parse_arguments(args2)
    assert parsed_args2.from_tm == "foo" and parsed_args2.to_sdf == "bar"


def make_test_output_dir():
    try:
        os.mkdir("test_output")
    except FileExistsError:
        pass


def test_sdf_example_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_sdf_to_wot_tm_from_path(
        "examples/sdf/example.sdf.json", "test_output/blah.tm.json"
    )


def test_wot_example_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_wot_tm_to_sdf_from_path(
        "examples/wot/example.tm.json", "test_output/blah.sdf.json"
    )


def test_wot_tm_td_example_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_wot_tm_to_wot_td_from_path(
        "examples/wot/example-with-bindings.tm.json", "test_output/blah.td.json"
    )


def test_wot_tm_td_placeholder_example_conversion():
    # TODO: Check for correct test output
    make_test_output_dir()
    convert_wot_tm_to_wot_td_from_path(
        "examples/wot/example-with-placeholders.tm.json",
        "test_output/blah_placeholders.td.json",
        placeholder_map_path="examples/wot/placeholders.json",
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
