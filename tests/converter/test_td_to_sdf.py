from sdf_wot_converter.converters import convert_sdf_to_wot_td


def perform_conversion_test(input, expected_result, **kwargs):
    sdf_model, sdf_mapping_file = input
    actual_result = convert_sdf_to_wot_td(
        sdf_model, sdf_mapping_files=[sdf_mapping_file], **kwargs
    )

    assert actual_result == expected_result


def test_empty_tm_sdf_conversion():

    input = [
        {
            "sdfObject": {
                "sdfObject0": {
                    "label": "MyLampThing",
                    "sdfProperty": {"status": {"observable": False, "type": "string"}},
                    "sdfAction": {"toggle": {}},
                    "sdfEvent": {"overheating": {"sdfOutputData": {"type": "string"}}},
                }
            },
            "namespace": {"saref": "https://w3id.org/saref#"},
        },
        {
            "map": {
                "#/sdfObject/sdfObject0/sdfProperty/status": {
                    "@type": "saref:OnOffState",
                    "forms": [{"href": "https://mylamp.example.com/status"}],
                },
                "#/sdfObject/sdfObject0/sdfAction/toggle": {
                    "@type": "saref:ToggleCommand",
                    "forms": [{"href": "https://mylamp.example.com/toggle"}],
                },
                "#/sdfObject/sdfObject0/sdfEvent/overheating": {
                    "forms": [{"href": "https://mylamp.example.com/oh"}]
                },
                "#/sdfObject/sdfObject0": {
                    "@context": [
                        "https://www.w3.org/2022/wot/td/v1.1",
                        {"saref": "https://w3id.org/saref#"},
                    ],
                    "id": "urn:dev:ops:32473-WoTLamp-1234",
                    "@type": ["saref:LightSwitch"],
                    "securityDefinitions": {
                        "basic_sc": {"scheme": "basic", "in": "header"}
                    },
                    "security": "basic_sc",
                },
            },
            "namespace": {"saref": "https://w3id.org/saref#"},
        },
    ]

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"saref": "https://w3id.org/saref#"},
        ],
        "@type": ["saref:LightSwitch"],
        "sdf:objectKey": "sdfObject0",
        "title": "MyLampThing",
        "actions": {
            "toggle": {
                "@type": "saref:ToggleCommand",
                "forms": [{"href": "https://mylamp.example.com/toggle"}],
            }
        },
        "properties": {
            "status": {
                "type": "string",
                "observable": False,
                "@type": "saref:OnOffState",
                "forms": [{"href": "https://mylamp.example.com/status"}],
            }
        },
        "events": {
            "overheating": {
                "data": {"type": "string"},
                "forms": [{"href": "https://mylamp.example.com/oh"}],
            }
        },
        "id": "urn:dev:ops:32473-WoTLamp-1234",
        "securityDefinitions": {"basic_sc": {"scheme": "basic", "in": "header"}},
        "security": "basic_sc",
    }

    perform_conversion_test(input, expected_result)
