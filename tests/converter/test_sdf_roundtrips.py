from sdf_wot_converter import convert_sdf_to_wot_tm
from sdf_wot_converter import convert_wot_tm_to_sdf
import pytest


def perform_sdf_roundtrip(input):
    converted_model = convert_sdf_to_wot_tm(input)
    result = convert_wot_tm_to_sdf(converted_model)

    assert input == result


def test_empty_sdf_tm_conversion():
    input = {}

    perform_sdf_roundtrip(input)
