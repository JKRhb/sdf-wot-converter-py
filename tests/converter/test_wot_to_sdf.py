from sdf_wot_converter import convert_wot_tm_to_sdf


def perform_conversion_test(input, expected_result):
    actual_result = convert_wot_tm_to_sdf(input)

    assert actual_result == expected_result


def test_empty_sdf_tm_conversion():

    input = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
    }

    expected_result = {}

    perform_conversion_test(input, expected_result)
