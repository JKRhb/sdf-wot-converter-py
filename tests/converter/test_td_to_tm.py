from sdf_wot_converter import convert_wot_td_to_wot_tm


def perform_conversion_test(input, expected_result, **kwargs):
    actual_result = convert_wot_td_to_wot_tm(input, **kwargs)

    assert actual_result == expected_result


def test_empty_td_tm_conversion():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    perform_conversion_test(input, expected_result)


def test_td_tm_conversion_with_thing_type():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": "tm:ThingModel",
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    perform_conversion_test(input, expected_result)


def test_td_tm_conversion_with_other_type():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "title": "Thing Title",
        "@type": "test",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": ["test", "tm:ThingModel"],
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    perform_conversion_test(input, expected_result)


def test_td_tm_conversion_with_thing_type_array():
    input = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "title": "Thing Title",
        "@type": ["test"],
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    expected_result = {
        "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
        "@type": ["test", "tm:ThingModel"],
        "title": "Thing Title",
        "security": ["nosec_sc"],
        "securityDefinitions": {"nosec_sc": {"scheme": "nosec"}},
    }

    perform_conversion_test(input, expected_result)
