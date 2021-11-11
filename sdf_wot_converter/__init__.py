import json
import argparse
import sys
import urllib.parse
import urllib.request
from jsonschema import Draft7Validator
from typing import Dict, Callable, Optional, List, Union

from sdf_wot_converter.converters.wot_common import flatten_thing_models
from .converters import (
    sdf_to_wot,
    wot_to_sdf,
    tm_to_td,
    td_to_tm,
)

from .schemas.sdf_validation_schema import sdf_validation_schema
from .schemas.td_schema import td_schema
from .schemas.tm_schema import tm_schema


def _load_model(input_path: str) -> Dict:  # pragma: no cover
    parsed_input_path = urllib.parse.urlparse(input_path)
    if parsed_input_path.scheme.startswith("http"):
        with urllib.request.urlopen(input_path) as url:
            retrieved_model = json.loads(url.read().decode())
            return retrieved_model
    else:
        file = open(input_path)
        return json.load(file)


def _save_model(output_path: str, model: Dict, indent=4):  # pragma: no cover
    file = open(output_path, "w")
    json.dump(model, file, indent=indent)


def _load_and_save_model(
    input_path: str,
    output_path: str,
    indent=4,
):  # pragma: no cover
    model = _load_model(input_path)
    _save_model(output_path, model, indent=indent)


def _load_optional_json_file(path: Optional[str]) -> Optional[Dict]:
    json_data = None
    if path:
        json_data = _load_model(path)

    return json_data


def _load_optional_json(json_string: Optional[str]) -> Optional[Dict]:
    json_data = None
    if json_string:
        json_data = json.loads(json_string)

    return json_data


def _convert_and_validate(
    from_model: Dict,
    from_schema: Dict,
    to_schema: Dict,
    converter_function: Callable,
    **kwargs,
):

    Draft7Validator(from_schema).validate(from_model)
    to_model = converter_function(from_model, **kwargs)
    Draft7Validator(to_schema).validate(to_model)
    return to_model


def _convert_model_from_path(
    from_path: str,
    to_path: str,
    from_schema: Dict,
    to_schema: Dict,
    converter_function: Callable,
    indent=4,
    **kwargs,
):  # pragma: no cover
    from_model = _load_model(from_path)
    to_model = _convert_and_validate(
        from_model,
        from_schema,
        to_schema,
        converter_function,
        **kwargs,
    )
    _save_model(to_path, to_model, indent=indent)


def _convert_model_from_json(
    from_model_json: str,
    from_schema: Dict,
    to_schema: Dict,
    converter_function: Callable,
    indent=4,
    **kwargs,
):  # pragma: no cover
    from_model = json.loads(from_model_json)
    to_model = _convert_and_validate(
        from_model,
        from_schema,
        to_schema,
        converter_function,
        **kwargs,
    )
    return json.dumps(to_model, indent=indent)


def convert_sdf_to_wot_tm(input: Dict, origin_url=None):
    return _convert_and_validate(
        input,
        sdf_validation_schema,
        tm_schema,
        sdf_to_wot.convert_sdf_to_wot_tm,
        origin_url=origin_url,
    )


def convert_wot_tm_to_sdf(input: Dict, placeholder_map=None):
    return _convert_and_validate(
        input,
        tm_schema,
        sdf_validation_schema,
        wot_to_sdf.convert_wot_tm_to_sdf,
        placeholder_map=placeholder_map,
    )


def convert_wot_tm_to_td(
    input: Dict, placeholder_map=None, meta_data=None, bindings=None
):
    return _convert_and_validate(
        input,
        tm_schema,
        td_schema,
        tm_to_td.convert_tm_to_td,
        placeholder_map=placeholder_map,
        meta_data=meta_data,
        bindings=bindings,
    )


def convert_wot_td_to_tm(input: Dict):
    return _convert_and_validate(input, td_schema, tm_schema, td_to_tm.convert_td_to_tm)


def convert_sdf_to_wot_tm_from_path(from_path: str, to_path: str, indent=4, **kwargs):
    return _convert_model_from_path(
        from_path,
        to_path,
        sdf_validation_schema,
        tm_schema,
        sdf_to_wot.convert_sdf_to_wot_tm,
        indent=indent,
        **kwargs,
    )


def convert_wot_tm_to_sdf_from_paths(
    from_paths: List[str],
    to_path: str,
    placeholder_map_path=None,
    indent=4,
):
    resolved_tms = _resolve_tm_input(from_paths, True)
    placeholder_map = _load_optional_json_file(placeholder_map_path)
    sdf_model = convert_wot_tm_to_sdf(resolved_tms, placeholder_map=placeholder_map)
    _save_model(to_path, sdf_model, indent=indent)


def convert_wot_tm_to_sdf_from_path(
    from_path: str, to_path: str, placeholder_map_path=None, indent=4
):

    placeholder_map = _load_optional_json_file(placeholder_map_path)
    return _convert_model_from_path(
        from_path,
        to_path,
        tm_schema,
        sdf_validation_schema,
        wot_to_sdf.convert_wot_tm_to_sdf,
        placeholder_map=placeholder_map,
        indent=indent,
    )


def convert_wot_tm_to_wot_td_from_path(
    from_path: str,
    to_path: str,
    placeholder_map_path=None,
    meta_data_path=None,
    bindings_path=None,
    indent=4,
):
    placeholder_map = _load_optional_json_file(placeholder_map_path)
    meta_data = _load_optional_json_file(meta_data_path)
    bindings = _load_optional_json_file(bindings_path)
    return _convert_model_from_path(
        from_path,
        to_path,
        tm_schema,
        td_schema,
        tm_to_td.convert_tm_to_td,
        placeholder_map=placeholder_map,
        meta_data=meta_data,
        bindings=bindings,
        indent=indent,
    )


def convert_wot_tm_to_td_from_paths(
    from_paths: List[str], to_path: str, placeholder_map_path=None, indent=4
):
    # TODO: Refactor
    resolved_tms = _resolve_tm_input(from_paths, True)
    placeholder_map = _load_optional_json_file(placeholder_map_path)
    sdf_model = convert_wot_tm_to_sdf(resolved_tms, placeholder_map=placeholder_map)
    _save_model(to_path, sdf_model, indent=indent)


def convert_wot_td_to_wot_tm_from_path(from_path: str, to_path: str, indent=4):
    return _convert_model_from_path(
        from_path,
        to_path,
        td_schema,
        tm_schema,
        td_to_tm.convert_td_to_tm,
        indent=indent,
    )


def convert_sdf_to_wot_tm_from_json(input: str, indent=4):
    return _convert_model_from_json(
        input,
        sdf_validation_schema,
        tm_schema,
        sdf_to_wot.convert_sdf_to_wot_tm,
        indent=indent,
    )


def convert_wot_tm_to_sdf_from_json(input: str, indent=4):

    return _convert_model_from_json(
        input,
        tm_schema,
        sdf_validation_schema,
        wot_to_sdf.convert_wot_tm_to_sdf,
        indent=indent,
    )


def convert_wot_tm_to_wot_td_from_json(
    input: str,
    indent=4,
    placeholder_map_json=None,
    meta_data_json=None,
    bindings_json=None,
):
    placeholder_map = _load_optional_json(placeholder_map_json)
    meta_data = _load_optional_json(meta_data_json)
    bindings = _load_optional_json(bindings_json)
    return _convert_model_from_json(
        input,
        tm_schema,
        td_schema,
        tm_to_td.convert_tm_to_td,
        indent=indent,
        placeholder_map=placeholder_map,
        meta_data=meta_data,
        bindings=bindings,
    )


def convert_wot_td_to_wot_tm_from_json(input: str, indent=4):
    return _convert_model_from_json(
        input,
        td_schema,
        tm_schema,
        td_to_tm.convert_td_to_tm,
        indent=indent,
    )


def _resolve_tm_input(thing_model_paths: List[str], resolve_extensions):
    thing_models = [_load_model(path) for path in thing_model_paths]
    flattened_thing_model = flatten_thing_models(thing_models, resolve_extensions)
    return flattened_thing_model


def _parse_arguments(args):
    # TODO: Argument structure might have to be reworked

    parser = argparse.ArgumentParser(
        description="Convert from SDF to WoT and vice versa."
    )

    from_group = parser.add_mutually_exclusive_group(required=True)
    from_group.add_argument(
        "--from-sdf", metavar="SDF", dest="from_sdf", help="SDF input JSON file"
    )
    from_group.add_argument(
        "--from-tm",
        metavar="TM",
        dest="from_tm",
        help="WoT TM input JSON file(s)",
        nargs="+",
    )
    from_group.add_argument(
        "--from-td", metavar="TD", dest="from_td", help="WoT TD input JSON file"
    )

    to_group = parser.add_mutually_exclusive_group(required=True)
    to_group.add_argument(
        "--to-tm", metavar="TM", dest="to_tm", help="WoT TM output file"
    )
    to_group.add_argument(
        "--to-td", metavar="TD", dest="to_td", help="WoT TD output file"
    )
    to_group.add_argument(
        "--to-sdf", metavar="SDF", dest="to_sdf", help="SDF output file"
    )

    parser.add_argument(
        "--placeholder",
        dest="placeholder_map",
        help="Optional placeholder map for TM-to-TD conversion",
    )

    parser.add_argument(
        "--meta-data",
        dest="meta_data",
        help="Additional meta-data for TM-to-TD conversion",
    )

    parser.add_argument(
        "--bindings",
        dest="bindings",
        help="Additional bindings information for TM-to-TD conversion",
    )

    parser.add_argument(
        "--no-extends",  # TODO: Might need a better name for this
        dest="no_extends",
        help="Don't resolve tm:extends links when using multiple TMs as input.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--origin-url", dest="origin_url", help="Explicitly set the model's origin URL."
    )

    parser.add_argument(
        "--indent",
        dest="indent",
        default=4,
        type=int,
        help="Indentation depth for the output JSON file.",
    )

    return parser.parse_args(args)


def get_origin_url(path: str, url: str):
    if url:
        return url
    elif path and (path.startswith("http://") or path.startswith("https://")):
        return path
    else:
        return None


def _use_converter_cli(args):  # pragma: no cover
    indent = args.indent
    if args.from_sdf:
        origin_url = get_origin_url(args.from_sdf, args.origin_url)
        if args.to_tm:
            convert_sdf_to_wot_tm_from_path(
                args.from_sdf, args.to_tm, indent=indent, origin_url=origin_url
            )
        elif args.to_sdf:
            _load_and_save_model(args.from_sdf, args.to_sdf, indent=indent)
        elif args.to_td:
            raise NotImplementedError("SDF -> TD conversion is not implemented, yet!")
    elif args.from_tm:
        if args.to_sdf:
            if len(args.from_tm) == 1:
                convert_wot_tm_to_sdf_from_path(
                    args.from_tm[0],
                    args.to_sdf,
                    placeholder_map_path=args.placeholder_map,
                    indent=indent,
                )
            else:
                convert_wot_tm_to_sdf_from_paths(
                    args.from_tm,
                    args.to_sdf,
                    placeholder_map_path=args.placeholder_map,
                    resolve_extensions=not args.no_extends,
                    indent=indent,
                )
        elif args.to_td:
            if len(args.from_tm) == 1:
                convert_wot_tm_to_wot_td_from_path(
                    args.from_tm[0],
                    args.to_td,
                    placeholder_map_path=args.placeholder_map,
                    meta_data_path=args.meta_data,
                    bindings_path=args.bindings,
                    indent=indent,
                )
            else:
                convert_wot_tm_to_td_from_paths(
                    args.from_tm,
                    args.to_sdf,
                    placeholder_map_path=args.placeholder_map,
                    indent=indent,
                )
        elif args.to_tm:
            if len(args.from_tm) == 1:
                _load_and_save_model(args.from_tm[0], args.to_tm)
            else:
                thing_model = _resolve_tm_input(args.from_tm, not args.no_extends)
                _save_model(args.to_tm, thing_model, indent=args.indent)
    elif args.from_td:
        if args.to_tm:
            convert_wot_td_to_wot_tm_from_path(
                args.from_td,
                args.to_tm,
                indent=indent,
            )
        elif args.to_td:
            _load_and_save_model(args.from_td, args.to_td, indent=indent)
        elif args.to_sdf:
            raise NotImplementedError("TD -> SDF conversion is not implemented, yet!")


def main():  # pragma: no cover
    args = _parse_arguments(sys.argv[1:])
    _use_converter_cli(args)
