from argparse import Namespace

import pytest
from sdf_wot_converter import parse_arguments, use_converter_cli
import os

from sdf_wot_converter.cli import CommandException, _get_origin_url


def test_parse_arguments():
    args1 = ["sdf-to-tm", "-i", "foo", "--mapping-files", "bar"]
    parsed_args1 = parse_arguments(args1)
    assert parsed_args1.sdf_model == "foo"
    assert parsed_args1.mapping_file_input_path == ["bar"]

    args2 = ["sdf-to-td", "-i", "foo", "--mapping-files", "bar"]
    parsed_args2 = parse_arguments(args2)
    assert parsed_args2.sdf_model == "foo"
    assert parsed_args2.mapping_file_input_path == ["bar"]

    args3 = ["tm-to-sdf", "-i", "foo"]
    parsed_args3 = parse_arguments(args3)
    assert parsed_args3.wot_tms == ["foo"]

    args4 = ["tm-to-td", "-i", "foo"]
    parsed_args4 = parse_arguments(args4)
    assert parsed_args4.wot_tms == ["foo"]

    args5 = ["td-to-tm", "-i", "foo"]
    parsed_args5 = parse_arguments(args5)
    assert parsed_args5.wot_tds == ["foo"]

    args6 = ["td-to-tm", "-i", "foo"]
    parsed_args6 = parse_arguments(args6)
    assert parsed_args6.wot_tds == ["foo"]


def make_test_output_dir():
    try:
        os.mkdir("test_output")
    except FileExistsError:
        pass


def test_sdf_example_conversion():

    make_test_output_dir()
    args = [
        "sdf-to-tm",
        "-i",
        "examples/sdf/example.sdf.json",
        "-o",
        "test_output/example-sdf.tm.json",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_sdf_to_td_example_conversion():

    make_test_output_dir()
    args = [
        "sdf-to-td",
        "-i",
        "examples/sdf/example.sdf.json",
        "--mapping-files",
        "examples/sdf/example.sdf-mapping.json",
        "-o",
        "test_output/example-sdf.td.json",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_wot_minimal_example_conversion():
    """Test for a WoT TM to SDF conversion, which does not lead to the creation of a
    mapping file."""

    make_test_output_dir()
    args = [
        "tm-to-sdf",
        "-i",
        "examples/wot/minimal-example.tm.jsonld",
        "-o",
        "test_output/example-tm.sdf.json",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_tm_sdf_minimal_example_print():
    """Test for a WoT TM to SDF conversion, printing out the outputs."""

    make_test_output_dir()
    args = [
        "tm-to-sdf",
        "-i",
        "examples/wot/minimal-example.tm.jsonld",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_wot_multiple_minimal_examples_conversion():
    """Test for a WoT TM to SDF conversion with multiple inputs, which does not lead to the creation of a
    mapping file."""

    make_test_output_dir()
    args = [
        "tm-to-sdf",
        "-i",
        "examples/wot/minimal-example.tm.jsonld",
        "examples/wot/minimal-example.tm.jsonld",
        "-o",
        "test_output/example-tm.sdf.json",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_wot_example_conversion():
    make_test_output_dir()
    args = [
        "tm-to-sdf",
        "-i",
        "examples/wot/example.tm.jsonld",
        "-o",
        "test_output/example-tm.sdf.json",
        "--mapping-file-output",
        "test_output/example-tm.sdf-mapping.json",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_tm_sdf_conversion_without_roundtripping():
    make_test_output_dir()
    args = [
        "--suppress-roundtripping",
        "tm-to-sdf",
        "-i",
        "examples/wot/minimal-example.tm.jsonld",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_multiple_tms_to_sdf_conversion():
    make_test_output_dir()
    args = [
        "tm-to-sdf",
        "-i",
        "examples/wot/example.tm.jsonld",
        "examples/wot/example-with-tm-extends.tm.jsonld",
        "-o",
        "test_output/multipleconvertedtms.sdf.json",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_wot_tm_td_example_conversion():
    make_test_output_dir()
    args = [
        "tm-to-td",
        "-i",
        "examples/wot/example-with-bindings.tm.jsonld",
        "-o",
        "test_output/blah.td.jsonld",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_multiple_tms_to_td_conversion():
    # TODO: Check how to apply bindings to Thing Collections.
    make_test_output_dir()
    args = [
        "tm-to-td",
        "-i",
        "examples/wot/example-with-bindings.tm.jsonld",
        "examples/wot/example-with-bindings.tm.jsonld",
        "-o",
        "test_output/multipleconvertedtms.td.jsonld",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_wot_tm_td_placeholder_example_conversion():
    make_test_output_dir()
    args = [
        "tm-to-td",
        "-i",
        "examples/wot/example-with-placeholders.tm.jsonld",
        "--placeholder-map",
        "examples/wot/placeholders.json",
        "-o",
        "test_output/example-with-placeholders.td.jsonld",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_wot_td_tm_example_conversion():
    make_test_output_dir()

    args = [
        "td-to-tm",
        "-i",
        "examples/wot/example.td.jsonld",
        "-o",
        "test_output/from_td.tm.jsonld",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_wot_td_sdf_example_conversion():
    make_test_output_dir()

    args = [
        "td-to-sdf",
        "-i",
        "examples/wot/example.td.jsonld",
        "-o",
        "test_output/example-td.sdf.json",
        "--mapping-file-output",
        "test_output/example-td.sdf-mapping.json",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_multiple_tds_to_td_conversion():
    make_test_output_dir()
    args = [
        "td-to-sdf",
        "-i",
        "examples/wot/example.td.jsonld",
        "examples/wot/example.td.jsonld",
        "-o",
        "test_output/multipleconvertedtds.td.jsonld",
        "--mapping-file-output",
        "test_output/multipleconvertedtds.sdf-mapping.json",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_wot_td_sdf_from_url_conversion():
    make_test_output_dir()

    args = [
        "td-to-sdf",
        "-i",
        "https://raw.githubusercontent.com/JKRhb/sdf-wot-converter-py/main/examples/wot/example.td.jsonld",
        "-o",
        "test_output/example-td-from-url.sdf.json",
        "--mapping-file-output",
        "test_output/example-td-from-url.sdf-mapping.json",
    ]
    parsed_args = parse_arguments(args)
    use_converter_cli(parsed_args)


def test_get_origin_url():
    assert _get_origin_url(None, None) is None
    assert _get_origin_url("http://example.com", None) == "http://example.com"
    assert _get_origin_url("https://example.com", None) == "https://example.com"
    assert _get_origin_url(None, "http://example.com") == "http://example.com"
    assert (
        _get_origin_url("http://hi.com", "http://example.com") == "http://example.com"
    )
    assert _get_origin_url("this/is/a/file/path", None) is None


def test_invalid_cli_arguments():
    with pytest.raises(CommandException):
        parsed_args = Namespace(
            command="td-to-td",
            indent=4,
            wot_tds=[],
            output_path=None,
            suppress_roundtripping=False,
        )
        use_converter_cli(parsed_args)
    with pytest.raises(CommandException):
        parsed_args = Namespace(
            command="tm-to-tm",
            indent=4,
            wot_tms=[],
            output_path=None,
            bindings=None,
            meta_data=None,
            placeholder_map=None,
            suppress_roundtripping=False,
        )
        use_converter_cli(parsed_args)
    with pytest.raises(CommandException):
        parsed_args = Namespace(
            command="sdf-to-sdf",
            indent=4,
            output_path="None",
            sdf_model="examples/sdf/example.sdf.json",
            mapping_file_input_path=None,
            origin_url=None,
            suppress_roundtripping=False,
        )
        use_converter_cli(parsed_args)
    with pytest.raises(CommandException):
        parsed_args = Namespace(command="unknown")
        use_converter_cli(parsed_args)
