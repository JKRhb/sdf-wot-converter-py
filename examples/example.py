from sdf_wot_converter.converters import (
    sdf_to_tm,
    tm_to_sdf,
)

sdf_model = {
    "info": {
        "title": "Example file for OneDM Semantic Definition Format",
        "version": "2019-04-24",
        "copyright": "Copyright 2019 Example Corp. All rights reserved.",
        "license": "https://example.com/license",
    },
    "namespace": {"cap": "https://example.com/capability/cap"},
    "defaultNamespace": "cap",
    "sdfObject": {
        "Switch": {
            "sdfProperty": {
                "value": {
                    "description": "The state of the switch; false for off and true for on.",
                    "type": "boolean",
                }
            },
            "sdfAction": {
                "on": {
                    "description": "Turn the switch on; equivalent to setting value to true."
                },
                "off": {
                    "description": "Turn the switch off; equivalent to setting value to false."
                },
                "toggle": {
                    "description": "Toggle the switch; equivalent to setting value to its complement."
                },
            },
        }
    },
}

thing_model = sdf_to_tm.convert_sdf_to_wot_tm(sdf_model)

expected_thing_model = {
    "@context": [
        "https://www.w3.org/2022/wot/td/v1.1",
        {
            "cap": "https://example.com/capability/cap",
            "sdf": "https://example.com/sdf",
        },
    ],
    "@type": "tm:ThingModel",
    "sdf:title": "Example file for OneDM Semantic Definition Format",
    "sdf:copyright": "Copyright 2019 Example Corp. All rights reserved.",
    "links": [{"href": "https://example.com/license", "rel": "license"}],
    "version": {"model": "2019-04-24"},
    "sdf:defaultNamespace": "cap",
    "actions": {
        "on": {
            "description": "Turn the switch on; equivalent to setting value to true.",
        },
        "off": {
            "description": "Turn the switch off; equivalent to setting value to false.",
        },
        "toggle": {
            "description": "Toggle the switch; equivalent to setting value to its complement.",
        },
    },
    "properties": {
        "value": {
            "description": "The state of the switch; false for off and true for on.",
            "type": "boolean",
        }
    },
    "sdf:objectKey": "Switch",
}

assert thing_model == expected_thing_model

sdf_roundtrip_model = tm_to_sdf.convert_wot_tm_to_sdf(thing_model)

assert sdf_model == sdf_roundtrip_model
