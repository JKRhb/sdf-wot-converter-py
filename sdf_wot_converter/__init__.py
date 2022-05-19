import argparse
import sys
from typing import Dict, List

from .io import (
    load_model,
    save_model,
    load_optional_json,
    load_optional_json_file,
    convert_model_from_path,
    convert_model_from_json,
    load_and_save_model,
)

from .converters.wot_common import flatten_thing_models
from .converters import (
    sdf_to_wot,
    wot_to_sdf,
    tm_to_td,
    td_to_tm,
)


def convert_wot_tm_to_td(
    input: Dict, placeholder_map=None, meta_data=None, bindings=None
):
    return tm_to_td.convert_tm_to_td(
        input, placeholder_map=placeholder_map, meta_data=meta_data, bindings=bindings
    )


def convert_wot_td_to_tm(input: Dict):
    return td_to_tm.convert_td_to_tm(input)


def convert_sdf_to_wot_tm_from_path(
    from_path: str, to_path: str, indent=4, origin_url=None
):
    from_model = load_model(from_path)
    to_model = sdf_to_wot.convert_sdf_to_wot_tm(from_model, origin_url=origin_url)

    save_model(to_path, to_model, indent=indent)


def convert_wot_tm_to_sdf_from_paths(
    from_paths: List[str],
    to_path: str,
    placeholder_map_path=None,
    indent=4,
):
    resolved_tms = _resolve_tm_input(from_paths, True)
    placeholder_map = load_optional_json_file(placeholder_map_path)
    sdf_model = wot_to_sdf.convert_wot_tm_to_sdf(
        resolved_tms, placeholder_map=placeholder_map
    )
    save_model(to_path, sdf_model, indent=indent)


def convert_wot_tm_to_sdf_from_path(
    from_path: str, to_path: str, placeholder_map_path=None, indent=4
):

    placeholder_map = load_optional_json_file(placeholder_map_path)
    return convert_model_from_path(
        from_path,
        to_path,
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
    placeholder_map = load_optional_json_file(placeholder_map_path)
    meta_data = load_optional_json_file(meta_data_path)
    bindings = load_optional_json_file(bindings_path)
    return convert_model_from_path(
        from_path,
        to_path,
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
    placeholder_map = load_optional_json_file(placeholder_map_path)
    sdf_model = wot_to_sdf.convert_wot_tm_to_sdf(
        resolved_tms, placeholder_map=placeholder_map
    )
    save_model(to_path, sdf_model, indent=indent)


def convert_wot_td_to_wot_tm_from_path(from_path: str, to_path: str, indent=4):
    return convert_model_from_path(
        from_path,
        to_path,
        td_to_tm.convert_td_to_tm,
        indent=indent,
    )


def convert_sdf_to_wot_tm_from_json(input: str, indent=4):
    return convert_model_from_json(
        input,
        sdf_to_wot.convert_sdf_to_wot_tm,
        indent=indent,
    )


def convert_wot_tm_to_sdf_from_json(input: str, indent=4):
    return convert_model_from_json(
        input,
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
    placeholder_map = load_optional_json(placeholder_map_json)
    meta_data = load_optional_json(meta_data_json)
    bindings = load_optional_json(bindings_json)
    return convert_model_from_json(
        input,
        tm_to_td.convert_tm_to_td,
        indent=indent,
        placeholder_map=placeholder_map,
        meta_data=meta_data,
        bindings=bindings,
    )


def convert_wot_td_to_wot_tm_from_json(input: str, indent=4):
    return convert_model_from_json(
        input,
        td_to_tm.convert_td_to_tm,
        indent=indent,
    )


# TODO: Turn into Thing Collection instead?
def _resolve_tm_input(thing_model_paths: List[str], resolve_extensions):
    thing_models = [load_model(path) for path in thing_model_paths]
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
            load_and_save_model(args.from_sdf, args.to_sdf, indent=indent)
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
                load_and_save_model(args.from_tm[0], args.to_tm)
            else:
                thing_model = _resolve_tm_input(args.from_tm, not args.no_extends)
                save_model(args.to_tm, thing_model, indent=args.indent)
    elif args.from_td:
        if args.to_tm:
            convert_wot_td_to_wot_tm_from_path(
                args.from_td,
                args.to_tm,
                indent=indent,
            )
        elif args.to_td:
            load_and_save_model(args.from_td, args.to_td, indent=indent)
        elif args.to_sdf:
            raise NotImplementedError("TD -> SDF conversion is not implemented, yet!")


def main():  # pragma: no cover
    args = _parse_arguments(sys.argv[1:])
    _use_converter_cli(args)
