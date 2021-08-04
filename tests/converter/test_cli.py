import json
from sdf_wot_converter import parse_arguments
from sdf_wot_converter import convert_sdf_to_wot_tm_from_path
from sdf_wot_converter import convert_wot_tm_to_sdf_from_path
from sdf_wot_converter import convert_sdf_to_wot_tm_from_json
from sdf_wot_converter import convert_wot_tm_to_sdf_from_json
import os


def test_parse_arguments():
    args1 = ["--from-sdf", "foo", "--to-tm", "bar"]
    parsed_args1 = parse_arguments(args1)
    assert parsed_args1.from_sdf == "foo" and parsed_args1.to_tm == "bar"

    args2 = ["--from-tm", "foo", "--to-sdf", "bar"]
    parsed_args2 = parse_arguments(args2)
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
