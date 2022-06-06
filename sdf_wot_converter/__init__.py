import sys
from .cli import parse_arguments, use_converter_cli

from .converters import (
    convert_wot_tm_to_sdf,
    convert_wot_tm_to_wot_td,
    convert_sdf_to_wot_td,
    convert_sdf_to_wot_tm,
    convert_wot_td_to_sdf,
    convert_wot_td_to_wot_tm,
)


def main():  # pragma: no cover
    args = parse_arguments(sys.argv[1:])
    use_converter_cli(args)
