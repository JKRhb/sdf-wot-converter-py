from sdf_wot_converter import convert_wot_tm_to_td


def perform_conversion_test(input, expected_result, placeholder_map=None):
    actual_result = convert_wot_tm_to_td(input, placeholder_map=placeholder_map)

    assert actual_result == expected_result


def test_empty_tm_td_conversion():
    # TODO: Handle case of TMs without title or security
    input = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": ["tm:ThingModel", "test"],
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td"],
        "@type": ["Thing", "test"],
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    perform_conversion_test(input, expected_result)

