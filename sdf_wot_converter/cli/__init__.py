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


def _load_single_model(paths_or_urls: Union[str, List[str]]) -> Dict:
    if isinstance(paths_or_urls, list):
        paths_or_urls = paths_or_urls[0]

    if validators.url(paths_or_urls):
        return _load_model_from_url(paths_or_urls)
    else:
        return _load_model_from_path(paths_or_urls)


def _load_model_or_collection(paths_or_urls: Union[str, List[str]], prefix: str):
    if isinstance(paths_or_urls, list) and len(paths_or_urls) == 1:
        paths_or_urls = paths_or_urls[0]

    if isinstance(paths_or_urls, str):
        return _load_single_model(paths_or_urls)

    result: Dict = {}

    for index, path_or_url in enumerate(paths_or_urls):
        result[f"{prefix}{index}"] = _load_single_model(path_or_url)

    return result


def _load_sdf_mapping_files(paths_or_urls: Optional[List[str]]) -> Optional[List[Dict]]:
    if paths_or_urls is None:
        return None

    result: List[Dict] = []

    for path_or_url in paths_or_urls:
        result.append(_load_single_model(path_or_url))

    return result


def save_or_print_model(output_path: Optional[str], model: Dict, indent=4):
    if output_path is not None:
        file = open(output_path, "w")
        json.dump(model, file, indent=indent)
        file.close()
    else:
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
        help="File paths or HTTP(S) URLs pointing to one or more SDF mapping files. "
        "These will be used during the conversion process to augment the given SDF model.",
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
        "sdf-to-tm", help="Converts an SDF model and mapping files to a WoT Thing Model"
    )
    sdf_to_wot_td = subparser.add_parser(
        "sdf-to-td",
        help="Converts an SDF model and mapping files to a WoT Thing Description",
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
        help="Converts a WoT Thing Description to an SDF model and mapping files",
    )
    wot_tm_to_wot_td = subparser.add_parser(
        "tm-to-td",
        help="Converts a WoT Thing Model to a WoT Thing Description.",
    )

    _add_mapping_file_output_argument(wot_tm_to_sdf)
    _add_output_argument(
        wot_tm_to_sdf,
        f"Output path for the converted SDF model and mapping files. {_output_path_help_text_suffix}",
    )
    _add_output_argument(
        wot_tm_to_wot_td,
        f"Output path for the converted WoT Thing Description. {_output_path_help_text_suffix}",
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
        "td-to-sdf", help="Converts a WoT Thing Model to an SDF model and mapping files"
    )
    wot_td_to_wot_tm = subparser.add_parser(
        "td-to-tm", help="Converts a WoT Thing Description to a WoT Thing Model"
    )

    _add_mapping_file_output_argument(wot_td_to_sdf)
    _add_output_argument(
        wot_td_to_sdf,
        f"Output path for the converted SDF model and mapping files. {_output_path_help_text_suffix}",
    )
    _add_output_argument(
        wot_td_to_wot_tm,
        f"Output path for the converted WoT Thing Model. {_output_path_help_text_suffix}",
    )

    for parser in [wot_td_to_sdf, wot_td_to_wot_tm]:
        _add_input_argument(
            parser,
            "One or more WoT Thing Descriptions (file paths or HTTP(S) URLs).",
            "WOT_TDS",
            "wot_tds",
            single_input=False,
        )


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description="Convert from SDF to WoT and vice versa."
    )

    subparser = parser.add_subparsers(dest="command")
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
        help='Suppresses the addition of additional fields for enabling roundtripping, like "sdf:objectKey".',
    )

    return parser.parse_args(args)


def _get_origin_url(path: str, url: str):
    if url:
        return url
    elif path and (path.startswith("http://") or path.startswith("https://")):
        return path
    else:
        return None


def _handle_from_sdf(args):
    indent = args.indent
    input_path = args.sdf_model
    output_path = args.output_path
    mapping_file_input_path = args.mapping_file_input_path
    command = args.command

    origin_url = _get_origin_url(input_path, args.origin_url)
    sdf_model = _load_single_model(input_path)
    sdf_mapping_files = _load_sdf_mapping_files(mapping_file_input_path)

    output = None
    if command == "sdf-to-td":
        output = convert_sdf_to_wot_td(
            sdf_model,
            origin_url=origin_url,
            sdf_mapping_files=sdf_mapping_files,
        )
    elif command == "sdf-to-tm":
        output = convert_sdf_to_wot_tm(
            sdf_model, sdf_mapping_files=sdf_mapping_files, origin_url=origin_url
        )

    save_or_print_model(output_path, output, indent=indent)


def _handle_from_tm(args):
    indent = args.indent

    command = args.command
    input_path = args.wot_tms
    output_path = args.output_path

    thing_models = _load_model_or_collection(input_path, "ThingModel")
    bindings = _load_optional_json_file(args.bindings)
    meta_data = _load_optional_json_file(args.meta_data)
    placeholder_map = _load_optional_json_file(args.placeholder_map)
    if command == "tm-to-sdf":
        output = convert_wot_tm_to_sdf(
            thing_models,
            placeholder_map=placeholder_map,
        )
        if isinstance(output, dict):
            save_or_print_model(output_path, output, indent=indent)
        else:
            mapping_file_output_path = args.mapping_file_output_path
            sdf_model, sdf_mapping_file = output

            save_or_print_model(output_path, sdf_model, indent=indent)
            save_or_print_model(
                mapping_file_output_path, sdf_mapping_file, indent=indent
            )

    elif command == "tm-to-td":
        output = convert_wot_tm_to_wot_td(
            thing_models,
            placeholder_map=placeholder_map,
            meta_data=meta_data,
            bindings=bindings,
        )

        save_or_print_model(output_path, output, indent=indent)


def _handle_from_td(args):
    indent = args.indent
    command = args.command

    thing_description = _load_model_or_collection(args.wot_tds, "ThingDescription")
    output_path = args.output_path
    if command == "td-to-tm":
        thing_model = convert_wot_td_to_wot_tm(thing_description)
        save_or_print_model(output_path, thing_model, indent=indent)
    elif command == "td-to-sdf":
        sdf_model, mapping_file = convert_wot_td_to_sdf(thing_description)
        save_or_print_model(output_path, sdf_model, indent=indent)
        save_or_print_model(args.mapping_file_output_path, mapping_file, indent=indent)


def _load_optional_json_file(path: Optional[str]) -> Optional[Dict]:
    json_data = None
    if path:
        json_data = _load_single_model(path)

    return json_data


def use_converter_cli(args):
    command = args.command
    if command.startswith("sdf-to"):
        _handle_from_sdf(args)
    elif command.startswith("tm-to"):
        _handle_from_tm(args)
    elif command.startswith("td-to"):
        _handle_from_td(args)


def main():  # pragma: no cover
    args = parse_arguments(sys.argv[1:])
    use_converter_cli(args)
