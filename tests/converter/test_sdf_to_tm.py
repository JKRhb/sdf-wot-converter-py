from jsonschema import ValidationError
import pytest

from sdf_wot_converter.converters.sdf_to_tm import add_origin_link
from sdf_wot_converter.converters.tm_to_sdf import convert_wot_tm_collection_to_sdf

from sdf_wot_converter import convert_wot_tm_to_sdf, convert_sdf_to_wot_tm


def perform_sdf_roundtrip_test(input):
    converted_model = convert_sdf_to_wot_tm(input)
    result = convert_wot_tm_to_sdf(converted_model)

    assert input == result[0]


def perform_sdf_thing_collection_roundtrip_test(
    input, root_model_key=None, top_model_keys=None
):
    converted_model = convert_sdf_to_wot_tm(input)
    result = convert_wot_tm_collection_to_sdf(
        converted_model, root_model_key=root_model_key, top_model_keys=top_model_keys
    )

    assert input == result[0]


def perform_conversion_test(input, expected_result, **kwargs):
    actual_result = convert_sdf_to_wot_tm(input, **kwargs)

    assert actual_result == expected_result


def test_empty_sdf_tm_conversion():
    input = {"sdfObject": {"Test": {}}}

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "sdf:objectKey": "Test",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_example_conversion():
    input = {
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
                "label": "Switch",
                "sdfProperty": {
                    "value": {
                        "description": "The state of the switch; false for off and true for on.",
                        "type": "boolean",
                        "observable": False,
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

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {
                "cap": "https://example.com/capability/cap",
                "sdf": "https://example.com/sdf",
            },
        ],
        "@type": "tm:ThingModel",
        "title": "Switch",
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
                "observable": False,
            }
        },
        "sdf:objectKey": "Switch",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_infoblock_conversion():
    input = {
        "info": {
            "title": "Test",
            "version": "2021-07-31",
            "copyright": "Copyright (c) 2021 Example Corp",
            "license": "BSD-3-Clause",
        },
        "sdfObject": {"Test": {}},
    }

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "sdf:title": "Test",
        "sdf:copyright": "Copyright (c) 2021 Example Corp",
        "sdf:license": "BSD-3-Clause",
        "version": {
            "model": "2021-07-31",
        },
        "sdf:objectKey": "Test",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_multiple_objects_and_things():
    input = {
        "sdfThing": {
            "testThing1": {
                "sdfObject": {"Test1": {}, "Test2": {}},
            },
            "testThing2": {
                "sdfObject": {"Test3": {}, "Test2": {}},
            },
        }
    }

    expected_result = {
        "sdfThing/testThing1": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:thingKey": "testThing1",
            "links": [
                {
                    "href": "#/sdfThing~1testThing1~1sdfObject~1Test1",
                    "rel": "tm:submodel",
                },
                {
                    "href": "#/sdfThing~1testThing1~1sdfObject~1Test2",
                    "rel": "tm:submodel",
                },
            ],
        },
        "sdfThing/testThing1/sdfObject/Test1": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:objectKey": "Test1",
        },
        "sdfThing/testThing1/sdfObject/Test2": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:objectKey": "Test2",
        },
        "sdfThing/testThing2": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:thingKey": "testThing2",
            "links": [
                {
                    "href": "#/sdfThing~1testThing2~1sdfObject~1Test3",
                    "rel": "tm:submodel",
                },
                {
                    "href": "#/sdfThing~1testThing2~1sdfObject~1Test2",
                    "rel": "tm:submodel",
                },
            ],
        },
        "sdfThing/testThing2/sdfObject/Test3": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:objectKey": "Test3",
        },
        "sdfThing/testThing2/sdfObject/Test2": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:objectKey": "Test2",
        },
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_thing_collection_roundtrip_test(
        input,
        root_model_key="sdfThing/testThing1",
        top_model_keys={"sdfThing/testThing1", "sdfThing/testThing2"},
    )


def test_sdf_tm_partial_infoblock_conversion():
    input = {
        "info": {"title": "Test"},
        "sdfObject": {"Test": {}},
    }

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "sdf:objectKey": "Test",
        "sdf:title": "Test",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_type_conversion():
    input = {
        "sdfObject": {
            "Test": {
                "label": "SdfTestObject",
                "description": "An sdfObject used for testing",
                "$comment": "This sdfObject is for testing only!",
                "sdfProperty": {
                    "foo": {
                        "label": "This is a label.",
                        "$comment": "This is a comment!",
                        "type": "integer",
                        "readable": True,
                        "observable": False,
                        "const": 5,
                        "default": 5,
                        "minimum": 0,
                        "maximum": 9002,
                        "exclusiveMinimum": 0,
                        "exclusiveMaximum": 9000,
                        "multipleOf": 2,
                    },
                    "bar": {
                        "type": "number",
                        "writable": True,
                        "observable": True,
                        "const": 5,
                        "unit": "C",
                        "default": 5,
                        "minimum": 0.0,
                        "maximum": 9002.0,
                        "exclusiveMinimum": 0.0,
                        "exclusiveMaximum": 9000.0,
                        "multipleOf": 2.0,
                    },
                    "baz": {
                        "type": "string",
                        "observable": False,
                        "minLength": 3,
                        "maxLength": 5,
                        "enum": ["hi", "hey"],
                        "pattern": "email",
                        "format": "uri-reference",
                        "contentFormat": "audio/mpeg",
                        "sdfType": "byte-string",
                    },
                    "foobar": {
                        "type": "array",
                        "observable": False,
                        "minItems": 2,
                        "maxItems": 5,
                        "uniqueItems": True,
                        "items": {"type": "string"},
                    },
                    "barfoo": {
                        "type": "object",
                        "observable": False,
                        "properties": {"foo": {"type": "string"}},
                        "required": ["foo"],
                        "nullable": True,
                    },
                },
            }
        }
    }

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "title": "SdfTestObject",
        "description": "An sdfObject used for testing",
        "sdf:$comment": "This sdfObject is for testing only!",
        "properties": {
            "foo": {
                "title": "This is a label.",
                "sdf:$comment": "This is a comment!",
                "writeOnly": False,
                "observable": False,
                "type": "integer",
                "const": 5,
                "default": 5,
                "minimum": 0,
                "maximum": 9002,
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 9000,
                "multipleOf": 2,
            },
            "bar": {
                "readOnly": False,
                "observable": True,
                "type": "number",
                "const": 5,
                "unit": "C",
                "default": 5,
                "minimum": 0.0,
                "maximum": 9002.0,
                "exclusiveMinimum": 0.0,
                "exclusiveMaximum": 9000.0,
                "multipleOf": 2.0,
            },
            "baz": {
                "type": "string",
                "observable": False,
                "minLength": 3,
                "maxLength": 5,
                "enum": ["hi", "hey"],
                "pattern": "email",
                "format": "uri-reference",
                "contentMediaType": "audio/mpeg",
                "sdf:sdfType": "byte-string",
            },
            "foobar": {
                "type": "array",
                "observable": False,
                "minItems": 2,
                "maxItems": 5,
                "items": {"type": "string"},
                "sdf:uniqueItems": True,
            },
            "barfoo": {
                "type": "object",
                "observable": False,
                "properties": {"foo": {"type": "string"}},
                "required": ["foo"],
                "sdf:nullable": True,
            },
        },
        "sdf:objectKey": "Test",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_action_conversion():
    input = {
        "sdfObject": {
            "Test": {
                "sdfAction": {
                    "foobar": {
                        "sdfInputData": {"type": "string"},
                        "sdfOutputData": {"type": "string"},
                    }
                }
            }
        }
    }
    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "actions": {
            "foobar": {
                "input": {"type": "string"},
                "output": {"type": "string"},
            }
        },
        "sdf:objectKey": "Test",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_event_conversion():
    input = {
        "sdfObject": {
            "Test": {
                "sdfEvent": {
                    "foobar": {"sdfOutputData": {"type": "string"}},
                    "foobaz": {},
                }
            }
        }
    }

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "events": {
            "foobar": {
                "data": {"type": "string"},
            },
            "foobaz": {},
        },
        "sdf:objectKey": "Test",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_sdf_ref_conversion():
    input = {
        "sdfObject": {
            "Test": {
                "sdfAction": {
                    "foobar": {"label": "hi"},
                    "foobaz": {"sdfRef": "#/sdfObject/Test/sdfAction/foobar"},
                },
                "sdfEvent": {
                    "foobar": {"label": "hi"},
                    "foobaz": {"sdfRef": "#/sdfObject/Test/sdfEvent/foobar"},
                },
                "sdfProperty": {
                    "foobar": {
                        "label": "hi",
                        "observable": False,
                    },
                    "foobaz": {
                        "sdfRef": "#/sdfObject/Test/sdfProperty/foobar",
                        "observable": False,
                    },
                },
            }
        }
    }

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "actions": {
            "foobar": {
                "title": "hi",
            },
            "foobaz": {
                "tm:ref": "#/actions/foobar",
            },
        },
        "properties": {
            "foobar": {
                "title": "hi",
                "observable": False,
            },
            "foobaz": {
                "observable": False,
                "tm:ref": "#/properties/foobar",
            },
        },
        "events": {
            "foobar": {
                "title": "hi",
            },
            "foobaz": {
                "tm:ref": "#/events/foobar",
            },
        },
        "sdf:objectKey": "Test",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_nested_model():
    input = {
        "sdfThing": {
            "blah": {
                "sdfThing": {
                    "foo": {
                        "sdfThing": {
                            "bar": {
                                "sdfObject": {
                                    "baz": {
                                        "sdfProperty": {
                                            "foobar": {
                                                "label": "hi",
                                                "observable": True,
                                            },
                                        },
                                        "sdfAction": {
                                            "foobar": {"label": "hi"},
                                        },
                                        "sdfEvent": {
                                            "foobar": {"label": "hi"},
                                        },
                                        "sdfRequired": [
                                            "#/sdfThing/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfProperty/foobar",
                                            "#/sdfThing/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfAction/foobar",
                                            "#/sdfThing/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfEvent/foobar",
                                        ],
                                    }
                                }
                            }
                        },
                    }
                },
            }
        }
    }

    expected_result = {
        "sdfThing/blah": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:thingKey": "blah",
            "links": [
                {"href": "#/sdfThing~1blah~1sdfThing~1foo", "rel": "tm:submodel"}
            ],
        },
        "sdfThing/blah/sdfThing/foo": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:thingKey": "foo",
            "links": [
                {
                    "href": "#/sdfThing~1blah~1sdfThing~1foo~1sdfThing~1bar",
                    "rel": "tm:submodel",
                }
            ],
        },
        "sdfThing/blah/sdfThing/foo/sdfThing/bar": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:thingKey": "bar",
            "links": [
                {
                    "href": "#/sdfThing~1blah~1sdfThing~1foo~1sdfThing~1bar~1sdfObject~1baz",
                    "rel": "tm:submodel",
                }
            ],
        },
        "sdfThing/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:objectKey": "baz",
            "tm:required": [
                "#/properties/foobar",
                "#/actions/foobar",
                "#/events/foobar",
            ],
            "actions": {"foobar": {"title": "hi"}},
            "properties": {"foobar": {"title": "hi", "observable": True}},
            "events": {"foobar": {"title": "hi"}},
        },
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_thing_collection_roundtrip_test(input)


def test_sdf_tm_looping_sdf_ref():
    input = {
        "sdfObject": {
            "Test": {
                "sdfProperty": {
                    "foo": {"sdfRef": "#/sdfObject/Test/sdfProperty/bar"},
                    "bar": {"sdfRef": "#/sdfObject/Test/sdfProperty/foo"},
                },
            }
        }
    }

    expected_result = None

    with pytest.raises(Exception) as e_info:
        perform_conversion_test(input, expected_result)

    assert (
        str(e_info.value)
        == "Encountered a looping sdfRef: #/sdfObject/Test/sdfProperty/bar"
    )


def test_sdf_tm_unparsabable_sdf_ref():
    input = {
        "sdfObject": {
            "Test": {
                "sdfProperty": {
                    "foo": {"sdfRef": "bla/sdfProperty/bar"},
                },
            }
        }
    }

    expected_result = None

    with pytest.raises(Exception) as e_info:
        perform_conversion_test(input, expected_result)

    assert str(e_info.value) == "sdfRef bla/sdfProperty/bar could not be resolved"


def test_sdf_tm_failing_URL_sdf_ref():
    input = {
        "namespace": {"bla": "https://example.org"},
        "sdfObject": {
            "Test": {
                "sdfProperty": {
                    "foo": {"sdfRef": "bla:/sdfProperty/bar"},
                },
            }
        },
    }

    expected_result = None

    with pytest.raises(Exception) as e_info:
        perform_conversion_test(input, expected_result)

    error_message = "No valid SDF model could be retrieved from https://example.org"

    assert str(e_info.value) == error_message


def test_sdf_tm_succeeding_URL_sdf_ref():
    test_url = "https://raw.githubusercontent.com/one-data-model/playground/master/sdfObject/sdfobject-accelerometer.sdf.json"

    input = {
        "namespace": {"test": test_url},
        "sdfObject": {
            "Test": {
                "sdfProperty": {
                    "foo": {
                        "sdfRef": "test:/sdfObject/Accelerometer/sdfProperty/X_Value"
                    },
                },
            }
        },
    }

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {
                "sdf": "https://example.com/sdf",
                "test": test_url,
            },
        ],
        "@type": "tm:ThingModel",
        "properties": {
            "foo": {
                "title": "X Value",
                "description": "The measured value along the X axis.",
                "readOnly": True,
                "type": "number",
                "observable": True,
            },
        },
        "sdf:objectKey": "Test",
    }

    perform_conversion_test(input, expected_result)


def test_sdf_tm_sdf_choice():
    input = {
        "sdfObject": {
            "Test": {
                "sdfProperty": {
                    "foobar": {
                        "observable": True,
                        "sdfChoice": {
                            "blah": {
                                "type": "string",
                            }
                        },
                    },
                    "foobaz": {
                        "observable": True,
                        "enum": ["blargh"],
                        "sdfChoice": {
                            "blah": {"type": "string"},
                            "foo": {"type": "number"},
                        },
                    },
                }
            }
        }
    }

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "properties": {
            "foobar": {
                "observable": True,
                "enum": [{"sdf:choiceName": "blah", "type": "string"}],
            },
            "foobaz": {
                "observable": True,
                "enum": [
                    "blargh",
                    {"sdf:choiceName": "blah", "type": "string"},
                    {"sdf:choiceName": "foo", "type": "number"},
                ],
            },
        },
        "sdf:objectKey": "Test",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_sdf_data_conversion():
    input = {
        "sdfObject": {
            "Test": {
                "sdfData": {
                    "fizz": {"type": "string"},
                },
                "sdfAction": {
                    "foobar": {
                        "label": "hi",
                        "sdfInputData": {"sdfRef": "#/sdfObject/Test/sdfData/fizz"},
                    },
                    "foobaz": {
                        "label": "hi",
                        "sdfInputData": {
                            "sdfRef": "#/sdfObject/Test/sdfAction/foobaz/sdfData/barfoo"
                        },
                        "sdfData": {
                            "barfoo": {"sdfRef": "#/sdfObject/Test/sdfData/fizz"}
                        },
                    },
                },
                "sdfEvent": {
                    "foobar": {
                        "label": "hi",
                        "sdfOutputData": {"sdfRef": "#/sdfObject/Test/sdfData/fizz"},
                    },
                    "foobaz": {
                        "label": "hi",
                        "sdfOutputData": {
                            "sdfRef": "#/sdfObject/Test/sdfEvent/foobaz/sdfData/barfoo"
                        },
                        "sdfData": {
                            "barfoo": {"sdfRef": "#/sdfObject/Test/sdfData/fizz"}
                        },
                    },
                },
            }
        }
    }

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {"sdf": "https://example.com/sdf"},
        ],
        "@type": "tm:ThingModel",
        "schemaDefinitions": {
            "fizz": {
                "type": "string",
            },
            "foobaz_barfoo_action": {
                "tm:ref": "#/schemaDefinitions/fizz",
            },
            "foobaz_barfoo_event": {
                "tm:ref": "#/schemaDefinitions/fizz",
            },
        },
        "actions": {
            "foobar": {
                "input": {"tm:ref": "#/schemaDefinitions/fizz"},
                "title": "hi",
            },
            "foobaz": {
                "title": "hi",
                "input": {"tm:ref": "#/schemaDefinitions/foobaz_barfoo_action"},
            },
        },
        "events": {
            "foobar": {
                "data": {"tm:ref": "#/schemaDefinitions/fizz"},
                "title": "hi",
            },
            "foobaz": {
                "title": "hi",
                "data": {"tm:ref": "#/schemaDefinitions/foobaz_barfoo_event"},
            },
        },
        "sdf:objectKey": "Test",
    }

    perform_conversion_test(input, expected_result)
    # TODO: Check if roundtripping can be made possible
    # perform_sdf_roundtrip_test(input)


def test_empty_namespace_conversion():
    input = {
        "namespace": {"cap": "https://example.com/capability/cap"},
        "defaultNamespace": "cap",
        "sdfObject": {
            "Test": {},
        },
    }

    expected_result = {
        "@context": [
            "https://www.w3.org/2022/wot/td/v1.1",
            {
                "sdf": "https://example.com/sdf",
                "cap": "https://example.com/capability/cap",
            },
        ],
        "sdf:defaultNamespace": "cap",
        "@type": "tm:ThingModel",
        "sdf:objectKey": "Test",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_add_origin_link():
    input1 = {}
    input2 = {"links": []}

    expected_result1 = {"links": [{"href": "https://example.org", "rel": "alternate"}]}

    add_origin_link(input1, origin_url="https://example.org")
    add_origin_link(input2, origin_url="https://example.org")
    assert input1 == expected_result1
    assert input2 == expected_result1


def test_sdf_tm_nested_sdf_conversion():
    input = {
        "sdfThing": {
            "foo": {
                "sdfProperty": {
                    "status": {
                        "observable": True,
                    }
                },
                "sdfObject": {"bar": {"sdfAction": {"toggle": {}}}},
            }
        },
        "sdfObject": {"baz": {}},
    }

    expected_result = {
        "sdfObject/baz": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:objectKey": "baz",
        },
        "sdfThing/foo": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:thingKey": "foo",
            "properties": {"status": {"observable": True}},
            "links": [
                {"href": "#/sdfThing~1foo~1sdfObject~1bar", "rel": "tm:submodel"}
            ],
        },
        "sdfThing/foo/sdfObject/bar": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {"sdf": "https://example.com/sdf"},
            ],
            "@type": "tm:ThingModel",
            "sdf:objectKey": "bar",
            "actions": {"toggle": {}},
        },
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_suppress_roundtripping_fields():
    input = {
        "info": {
            "license": "MIT",
            "title": "Test",
            "copyright": "2022 Example Corp",
        },
        "sdfThing": {
            "foo": {
                "sdfProperty": {
                    "status": {
                        "observable": True,
                        "sdfChoice": {"test": {"type": "string"}},
                    },
                },
                "sdfObject": {"bar": {"sdfAction": {"toggle": {}}}},
            }
        },
        "sdfObject": {"baz": {}},
    }

    expected_result = {
        "sdfObject/baz": {
            "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
            "@type": "tm:ThingModel",
        },
        "sdfThing/foo": {
            "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
            "@type": "tm:ThingModel",
            "properties": {
                "status": {"enum": [{"type": "string"}], "observable": True}
            },
            "links": [
                {"href": "#/sdfThing~1foo~1sdfObject~1bar", "rel": "tm:submodel"}
            ],
        },
        "sdfThing/foo/sdfObject/bar": {
            "@context": ["https://www.w3.org/2022/wot/td/v1.1"],
            "@type": "tm:ThingModel",
            "actions": {"toggle": {}},
        },
    }

    perform_conversion_test(input, expected_result, suppress_roundtripping=True)


def test_td_tm_illegal_input():
    input = {"info": "hello"}

    with pytest.raises(ValidationError):
        convert_sdf_to_wot_tm(input)


def test_sdf_tm_duplicate_keys():

    input = {
        "info": {
            "title": "Example file for OneDM Semantic Definition Format",
            "version": "2019-04-24",
            "copyright": "Copyright 2019 Example Corp. All rights reserved.",
            "license": "https://example.com/license",
        },
        "namespace": {"cap": "https://example.com/capability/cap"},
        "defaultNamespace": "cap",
        "sdfThing": {
            "Switch": {
                "sdfThing": {
                    "Switch": {
                        "sdfObject": {
                            "Switch": {
                                "sdfProperty": {
                                    "value": {
                                        "description": "The state of the switch; false for off and true for on.",
                                        "type": "boolean",
                                        "observable": True,
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
                        }
                    }
                }
            }
        },
    }

    expected_result = {
        "sdfThing/Switch": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {
                    "cap": "https://example.com/capability/cap",
                    "sdf": "https://example.com/sdf",
                },
            ],
            "@type": "tm:ThingModel",
            "sdf:thingKey": "Switch",
            "sdf:title": "Example file for OneDM Semantic Definition Format",
            "sdf:copyright": "Copyright 2019 Example Corp. All rights reserved.",
            "links": [
                {"href": "https://example.com/license", "rel": "license"},
                {"href": "#/sdfThing~1Switch~1sdfThing~1Switch", "rel": "tm:submodel"},
            ],
            "version": {"model": "2019-04-24"},
            "sdf:defaultNamespace": "cap",
        },
        "sdfThing/Switch/sdfThing/Switch": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {
                    "cap": "https://example.com/capability/cap",
                    "sdf": "https://example.com/sdf",
                },
            ],
            "@type": "tm:ThingModel",
            "sdf:thingKey": "Switch",
            "sdf:title": "Example file for OneDM Semantic Definition Format",
            "sdf:copyright": "Copyright 2019 Example Corp. All rights reserved.",
            "links": [
                {"href": "https://example.com/license", "rel": "license"},
                {
                    "href": "#/sdfThing~1Switch~1sdfThing~1Switch~1sdfObject~1Switch",
                    "rel": "tm:submodel",
                },
            ],
            "version": {"model": "2019-04-24"},
            "sdf:defaultNamespace": "cap",
        },
        "sdfThing/Switch/sdfThing/Switch/sdfObject/Switch": {
            "@context": [
                "https://www.w3.org/2022/wot/td/v1.1",
                {
                    "cap": "https://example.com/capability/cap",
                    "sdf": "https://example.com/sdf",
                },
            ],
            "@type": "tm:ThingModel",
            "sdf:objectKey": "Switch",
            "sdf:title": "Example file for OneDM Semantic Definition Format",
            "sdf:copyright": "Copyright 2019 Example Corp. All rights reserved.",
            "links": [{"href": "https://example.com/license", "rel": "license"}],
            "version": {"model": "2019-04-24"},
            "sdf:defaultNamespace": "cap",
            "actions": {
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
            "properties": {
                "value": {
                    "description": "The state of the switch; false for off and true for on.",
                    "type": "boolean",
                    "observable": True,
                }
            },
        },
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)
