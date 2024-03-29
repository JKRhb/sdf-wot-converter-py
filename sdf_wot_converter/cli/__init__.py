import argparse
import json
from pprint import pprint
import sys
from typing import Dict, List, Optional, Union
import urllib.request
import validators

from ..converters import (
    convert_sdf_to_wot_td,
    convert_sdf_to_wot_tm,
    convert_wot_td_to_sdf,
    convert_wot_td_to_wot_tm,
    convert_wot_tm_to_sdf,
    convert_wot_tm_to_wot_td,
)


class CommandException(Exception):
    """Is raised when an unknown command is passed to the CLI.
    Should never be raised in practice."""

    pass


_sdf_input_help_text = (
    "The SDF model that is supposed to be converted. "
    "Can either be a file path or a URL."
)

_output_path_help_text_suffix = (
    "If omitted, the result will be printed to the standard output instead."
)


def _load_model_from_path(input_path: str) -> Dict:
    file = open(input_path)
    return json.load(file)


def _load_model_from_url(input_url: str) -> Dict:
    with urllib.request.urlopen(input_url) as url:
        retrieved_model = json.loads(url.read().decode())
        return retrieved_model


def _load_model(paths_or_urls: str) -> Dict:
    if validators.url(paths_or_urls):
        return _load_model_from_url(paths_or_urls)
    else:
        return _load_model_from_path(paths_or_urls)


def _load_model_or_collection(paths_or_urls: Union[str, List[str]], prefix: str):
    if isinstance(paths_or_urls, list) and len(paths_or_urls) == 1:
        paths_or_urls = paths_or_urls[0]

    if isinstance(paths_or_urls, str):
        return _load_model(paths_or_urls)

    result: Dict = {}

    for index, path_or_url in enumerate(paths_or_urls):
        result[f"{prefix}{index}"] = _load_model(path_or_url)

    return result


def _load_sdf_mapping_files(paths_or_urls: Optional[List[str]]) -> Optional[List[Dict]]:
    if paths_or_urls is None:
        return None

    result: List[Dict] = []

    for path_or_url in paths_or_urls:
        result.append(_load_model(path_or_url))

    return result


def save_model(output_path: str, model: Dict, indent=4):
    file = open(output_path, "w")
    json.dump(model, file, indent=indent)
    file.close()


def save_or_print_model(
    output_path: Optional[str],
    model: Optional[Dict],
    indent=4,
    print_enabled=True,
):
    if model is None:
        return

    if output_path is not None:
        save_model(output_path, model, indent=indent)
    elif print_enabled:
        pprint(model, indent=indent)


def _add_input_argument(
    parser, help_text: str, metavar: str, dest: str, single_input=True
):
    nargs = None
    if not single_input:
        nargs = "*"

    parser.add_argument(
        "--input",
        "-i",
        metavar=metavar,
        dest=dest,
        type=str,
        help=help_text,
        required=True,
        nargs=nargs,
    )


def _add_output_argument(parser, help_text):
    parser.add_argument(
        "--output",
        "-o",
        nargs="?",
        dest="output_path",
        help=help_text,
    )


def _add_mapping_file_input_argument(parser):
    parser.add_argument(
        "--mapping-files",
        nargs="*",
        dest="mapping_file_input_path",
        help=(
            "File paths or HTTP(S) URLs pointing to one or more SDF mapping files. "
            "These will be used during the conversion process to augment the given "
            "SDF model."
        ),
    )


def _add_mapping_file_output_argument(subparser):
    subparser.add_argument(
        "--mapping-file-output",
        dest="mapping_file_output_path",
        help="Output path for SDF mapping files during the Wot to SDF process.",
    )


def _add_origin_url(parser):
    parser.add_argument(
        "--origin-url",
        dest="origin_url",
        type=str,
        help="Explicitly set the model's origin URL.",
    )


def _add_sdf_arguments(subparser):
    sdf_to_wot_tm = subparser.add_parser(
        "sdf-to-tm",
        help="Converts an SDF model and mapping files to one or WoT Thing Models.",
    )
    sdf_to_wot_td = subparser.add_parser(
        "sdf-to-td",
        help=(
            "Converts an SDF model and mapping files to one or more WoT Thing "
            "Descriptions."
        ),
    )

    _add_output_argument(
        sdf_to_wot_td,
        f"Output path for the converted WoT TD. {_output_path_help_text_suffix}",
    )
    _add_output_argument(
        sdf_to_wot_tm,
        f"Output path for the converted WoT TM. {_output_path_help_text_suffix}",
    )

    for parser in [sdf_to_wot_td, sdf_to_wot_tm]:
        _add_input_argument(parser, _sdf_input_help_text, "SDF_MODEL", "sdf_model")
        _add_mapping_file_input_argument(parser)
        _add_origin_url(parser)


def _add_tm_arguments(subparser):
    wot_tm_to_sdf = subparser.add_parser(
        "tm-to-sdf",
        help=(
            "Converts a WoT Thing Model to an SDF model and zero or more mapping "
            "files."
        ),
    )
    wot_tm_to_wot_td = subparser.add_parser(
        "tm-to-td",
        help="Converts a WoT Thing Model to a WoT Thing Description.",
    )

    _add_mapping_file_output_argument(wot_tm_to_sdf)
    _add_sdf_infoblock_arguments(wot_tm_to_sdf)
    _add_output_argument(
        wot_tm_to_sdf,
        "Output path for the converted SDF model and mapping files. "
        f"{_output_path_help_text_suffix}",
    )
    _add_output_argument(
        wot_tm_to_wot_td,
        "Output path for the converted WoT Thing Description. "
        f"{_output_path_help_text_suffix}",
    )

    wot_tm_to_wot_td.add_argument(
        "--remove-not-required-affordances",
        action="store_true",
        help="Lets the converter remove all affordances which do not appear in a "
        "tm:required array.",
    )

    for parser in [wot_tm_to_sdf, wot_tm_to_wot_td]:
        _add_input_argument(
            parser,
            "One or more WoT Thing models (file paths or HTTP(S) URLs).",
            "WOT_TMS",
            "wot_tms",
            single_input=False,
        )
        parser.add_argument(
            "--meta-data",
            dest="meta_data",
            help="Additional meta-data for TM conversion.",
        )

        parser.add_argument(
            "--bindings",
            dest="bindings",
            help="Additional bindings information for TM conversion.",
        )

        parser.add_argument(
            "--placeholder-map",
            dest="placeholder_map",
            help="Optional placeholder map for TM conversion.",
        )


def _add_td_arguments(subparser):
    wot_td_to_sdf = subparser.add_parser(
        "td-to-sdf",
        help="Converts one or more WoT Thing Models to an SDF model and zero or more "
        "mapping files.",
    )
    wot_td_to_wot_tm = subparser.add_parser(
        "td-to-tm",
        help="Converts one or more WoT Thing Descriptions to one or more WoT "
        "Thing Models.",
    )

    _add_mapping_file_output_argument(wot_td_to_sdf)
    _add_sdf_infoblock_arguments(wot_td_to_sdf)
    _add_output_argument(
        wot_td_to_sdf,
        "Output path for the converted SDF model and mapping files. "
        f"{_output_path_help_text_suffix}",
    )
    _add_output_argument(
        wot_td_to_wot_tm,
        "Output path for the converted WoT Thing Model. "
        f"{_output_path_help_text_suffix}",
    )

    for parser in [wot_td_to_sdf, wot_td_to_wot_tm]:
        _add_input_argument(
            parser,
            "One or more WoT Thing Descriptions (file paths or HTTP(S) URLs).",
            "WOT_TDS",
            "wot_tds",
            single_input=False,
        )


def _add_sdf_infoblock_arguments(parser):
    parser.add_argument(
        "--title",
        dest="sdf_title",
        help="Set the title for the  resulting SDF definitions.",
    )

    parser.add_argument(
        "--version",
        dest="sdf_version",
        help="Set the version for the  resulting SDF definitions.",
    )

    parser.add_argument(
        "--copyright",
        dest="sdf_copyright",
        help="Set the copyright for the resulting SDF definitions.",
    )

    parser.add_argument(
        "--license",
        dest="sdf_license",
        help="Set the license for the resulting SDF definitions.",
    )


def _get_sdf_infoblock(args) -> Optional[Dict]:
    title = args.sdf_title
    license = args.sdf_license
    version = args.sdf_version
    copyright = args.sdf_copyright

    infoblock = {}

    for key, value in [
        ("title", title),
        ("version", version),
        ("copyright", copyright),
        ("license", license),
    ]:
        if value is not None:
            infoblock[key] = value

    if len(infoblock) == 0:
        return None

    return infoblock


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description="Convert from SDF to WoT and vice versa."
    )

    subparser = parser.add_subparsers(dest="command", required=True)
    _add_sdf_arguments(subparser)
    _add_tm_arguments(subparser)
    _add_td_arguments(subparser)

    parser.add_argument(
        "--indent",
        dest="indent",
        default=4,
        type=int,
        help="Indentation depth for the output JSON files.",
    )

    parser.add_argument(
        "--suppress-roundtripping",
        action="store_true",
        help="Suppresses the addition of additional fields for enabling roundtripping, "
        'like "sdf:objectKey".',
    )

    return parser.parse_args(args)


def _get_origin_url(path: str, url: Optional[str]):
    if url is not None:
        return url
    elif path is not None and (
        path.startswith("http://") or path.startswith("https://")
    ):
        return path
    else:
        return None


def _handle_from_sdf(args):
    indent = args.indent
    input_path = args.sdf_model
    output_path = args.output_path
    mapping_file_input_path = args.mapping_file_input_path
    command = args.command
    suppress_roundtripping = args.suppress_roundtripping

    origin_url = _get_origin_url(input_path, args.origin_url)
    sdf_model = _load_model(input_path)
    sdf_mapping_files = _load_sdf_mapping_files(mapping_file_input_path)

    output = None
    if command == "sdf-to-td":
        output = convert_sdf_to_wot_td(
            sdf_model,
            origin_url=origin_url,
            sdf_mapping_files=sdf_mapping_files,
            suppress_roundtripping=suppress_roundtripping,
        )
    elif command == "sdf-to-tm":
        output = convert_sdf_to_wot_tm(
            sdf_model,
            sdf_mapping_files=sdf_mapping_files,
            origin_url=origin_url,
            suppress_roundtripping=suppress_roundtripping,
        )
    else:
        raise CommandException()

    save_or_print_model(output_path, output, indent=indent)


def _handle_from_tm(args):
    indent = args.indent

    command = args.command
    input_path = args.wot_tms
    output_path = args.output_path
    suppress_roundtripping = args.suppress_roundtripping

    thing_models = _load_model_or_collection(input_path, "ThingModel")
    bindings = _load_optional_json_file(args.bindings)
    meta_data = _load_optional_json_file(args.meta_data)
    placeholder_map = _load_optional_json_file(args.placeholder_map)
    if command == "tm-to-sdf":
        infoblock = _get_sdf_infoblock(args)
        output = convert_wot_tm_to_sdf(
            thing_models,
            placeholder_map=placeholder_map,
            suppress_roundtripping=suppress_roundtripping,
            infoblock=infoblock,
        )
        mapping_file_output_path = args.mapping_file_output_path
        if isinstance(output, dict):
            sdf_model, sdf_mapping_file = output, None
        else:
            sdf_model, sdf_mapping_file = output

        save_or_print_model(output_path, sdf_model, indent=indent)

        print_enabled = output_path is None
        save_or_print_model(
            mapping_file_output_path,
            sdf_mapping_file,
            indent=indent,
            print_enabled=print_enabled,
        )

    elif command == "tm-to-td":
        remove_not_required_affordances = args.remove_not_required_affordances
        output = convert_wot_tm_to_wot_td(
            thing_models,
            placeholder_map=placeholder_map,
            meta_data=meta_data,
            bindings=bindings,
            remove_not_required_affordances=remove_not_required_affordances,
        )

        save_or_print_model(output_path, output, indent=indent)

    else:
        raise CommandException()


def _handle_from_td(args):
    indent = args.indent
    command = args.command
    suppress_roundtripping = args.suppress_roundtripping

    thing_description = _load_model_or_collection(args.wot_tds, "ThingDescription")
    output_path = args.output_path
    if command == "td-to-tm":
        thing_model = convert_wot_td_to_wot_tm(thing_description)
        save_or_print_model(output_path, thing_model, indent=indent)
    elif command == "td-to-sdf":
        infoblock = _get_sdf_infoblock(args)
        sdf_model, mapping_file = convert_wot_td_to_sdf(
            thing_description,
            suppress_roundtripping=suppress_roundtripping,
            infoblock=infoblock,
        )
        save_or_print_model(output_path, sdf_model, indent=indent)

        print_enabled = output_path is None
        save_or_print_model(
            args.mapping_file_output_path,
            mapping_file,
            indent=indent,
            print_enabled=print_enabled,
        )
    else:
        raise CommandException()


def _load_optional_json_file(path: Optional[str]) -> Optional[Dict]:
    if path is None:
        return None

    return _load_model(path)


def use_converter_cli(args):
    command = args.command
    if command.startswith("sdf-to"):
        _handle_from_sdf(args)
    elif command.startswith("tm-to"):
        _handle_from_tm(args)
    elif command.startswith("td-to"):
        _handle_from_td(args)
    else:
        raise CommandException()


def main():  # pragma: no cover
    args = parse_arguments(sys.argv[1:])
    use_converter_cli(args)
