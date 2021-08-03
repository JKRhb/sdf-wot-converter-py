from converter import parse_arguments
from converter import convert_sdf_to_wot_tm_from_path
from converter import convert_wot_tm_to_sdf_from_path
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
    convert_wot_tm_to_sdf_from_path("examples/wot/example.tm.json", "test_output/blah.sdf.json")
