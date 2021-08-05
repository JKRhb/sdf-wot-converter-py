from sdf_wot_converter import convert_sdf_to_wot_tm
from sdf_wot_converter import convert_wot_tm_to_sdf
import pytest


def perform_sdf_roundtrip_test(input):
    converted_model = convert_sdf_to_wot_tm(input)
    result = convert_wot_tm_to_sdf(converted_model)

    assert input == result


def perform_conversion_test(input, expected_result):
    actual_result = convert_sdf_to_wot_tm(input)

    assert actual_result == expected_result


def test_empty_sdf_tm_conversion():
    input = {}

    expected_result = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test__sdf_tm_infoblock_conversion():
    input = {
        "info": {
            "title": "Test",
            "version": "2021-07-31",
            "copyright": "Copyright (c) 2021 Example Corp",
            "license": "https://example.com/LICENSE",
        }
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "title": "Test",
        "description": "Copyright (c) 2021 Example Corp",
        "version": {
            "model": "2021-07-31",
        },
        "links": [{"href": "https://example.com/LICENSE", "rel": "license"}],
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_type_conversion():
    input = {
        "sdfProperty": {
            "foo": {
                "label": "This is a label.",
                "$comment": "This is a comment!",
                "type": "integer",
                "readable": True,
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
                "minLength": 3,
                "maxLength": 5,
                "enum": ["hi", "hey"],
                "pattern": "email",
                "format": "uri-reference",
                "contentFormat": "audio/mpeg",
            },
            "foobar": {
                "type": "array",
                "minItems": 2,
                "maxItems": 5,
                "uniqueItems": True,
                "items": {"type": "string"},
            },
            "barfoo": {
                "type": "object",
                "properties": {"foo": {"type": "string", "observable": True}},
                "required": ["foo"],
            },
        }
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "properties": {
            "foo": {
                "title": "This is a label.",
                "sdf:$comment": "This is a comment!",
                "writeOnly": False,
                "type": "integer",
                "const": 5,
                "default": 5,
                "minimum": 0,
                "maximum": 9002,
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 9000,
                "multipleOf": 2,
                "sdf:jsonPointer": "#/sdfProperty/foo",
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
                "sdf:jsonPointer": "#/sdfProperty/bar",
            },
            "baz": {
                "type": "string",
                "minLength": 3,
                "maxLength": 5,
                "enum": ["hi", "hey"],
                "pattern": "email",
                "format": "uri-reference",
                "contentMediaType": "audio/mpeg",
                "sdf:jsonPointer": "#/sdfProperty/baz",
            },
            "foobar": {
                "type": "array",
                "minItems": 2,
                "maxItems": 5,
                "items": {"type": "string"},
                "uniqueItems": True,
                "sdf:jsonPointer": "#/sdfProperty/foobar",
            },
            "barfoo": {
                "type": "object",
                "properties": {"foo": {"type": "string", "sdf:observable": True}},
                "required": ["foo"],
                "sdf:jsonPointer": "#/sdfProperty/barfoo",
            },
        },
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_action_conversion():
    input = {
        "sdfAction": {
            "foobar": {
                "sdfInputData": {"type": "string"},
                "sdfOutputData": {"type": "string"},
            }
        }
    }
    expected_result = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "actions": {
            "foobar": {
                "sdf:jsonPointer": "#/sdfAction/foobar",
                "input": {"type": "string"},
                "output": {"type": "string"},
            }
        },
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_event_conversion():
    input = {"sdfEvent": {"foobar": {"sdfOutputData": {"type": "string"}}}}

    expected_result = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "events": {
            "foobar": {
                "data": {"type": "string"},
                "sdf:jsonPointer": "#/sdfEvent/foobar",
            }
        },
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)


def test_sdf_tm_sdf_ref_conversion():
    input = {
        "sdfAction": {
            "foobar": {"label": "hi"},
            "foobaz": {"sdfRef": "#/sdfAction/foobar"},
        },
        "sdfEvent": {
            "foobar": {"label": "hi"},
            "foobaz": {"sdfRef": "#/sdfEvent/foobar"},
        },
        "sdfProperty": {
            "foobar": {"label": "hi"},
            "foobaz": {"sdfRef": "#/sdfProperty/foobar"},
        },
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "actions": {
            "foobar": {"sdf:jsonPointer": "#/sdfAction/foobar", "title": "hi"},
            "foobaz": {
                "sdf:jsonPointer": "#/sdfAction/foobaz",
                "tm:ref": "#/actions/foobar",
            },
        },
        "properties": {
            "foobar": {"sdf:jsonPointer": "#/sdfProperty/foobar", "title": "hi"},
            "foobaz": {
                "sdf:jsonPointer": "#/sdfProperty/foobaz",
                "tm:ref": "#/properties/foobar",
            },
        },
        "events": {
            "foobar": {"sdf:jsonPointer": "#/sdfEvent/foobar", "title": "hi"},
            "foobaz": {
                "sdf:jsonPointer": "#/sdfEvent/foobaz",
                "tm:ref": "#/events/foobar",
            },
        },
    }

    perform_conversion_test(input, expected_result)


def test_sdf_tm_nested_model():
    input = {
        "sdfProduct": {
            "blah": {
                "sdfThing": {
                    "foo": {
                        "sdfRequired": [
                            "#/sdfProduct/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfProperty/foobar",
                            "#/sdfProduct/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfAction/foobar",
                            "#/sdfProduct/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfEvent/foobar",
                        ],
                        "sdfThing": {
                            "bar": {
                                "sdfObject": {
                                    "baz": {
                                        "sdfProperty": {
                                            "foobar": {"label": "hi"},
                                        },
                                        "sdfAction": {
                                            "foobar": {"label": "hi"},
                                        },
                                        "sdfEvent": {
                                            "foobar": {"label": "hi"},
                                        },
                                    }
                                }
                            }
                        },
                    }
                }
            }
        }
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "actions": {
            "blah_foo_bar_baz_foobar": {
                "sdf:jsonPointer": "#/sdfProduct/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfAction/foobar",
                "title": "hi",
            },
        },
        "properties": {
            "blah_foo_bar_baz_foobar": {
                "sdf:jsonPointer": "#/sdfProduct/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfProperty/foobar",
                "title": "hi",
            },
        },
        "events": {
            "blah_foo_bar_baz_foobar": {
                "sdf:jsonPointer": "#/sdfProduct/blah/sdfThing/foo/sdfThing/bar/sdfObject/baz/sdfEvent/foobar",
                "title": "hi",
            },
        },
        "tm:required": [
            "#/properties/blah_foo_bar_baz_foobar",
            "#/actions/blah_foo_bar_baz_foobar",
            "#/events/blah_foo_bar_baz_foobar",
        ],
    }

    perform_conversion_test(input, expected_result)


def test_sdf_tm_looping_sdf_ref():
    input = {
        "sdfProperty": {
            "foo": {"sdfRef": "#/sdfProperty/bar"},
            "bar": {"sdfRef": "#/sdfProperty/foo"},
        },
    }

    expected_result = None

    with pytest.raises(Exception) as e_info:
        perform_conversion_test(input, expected_result)

    assert str(e_info.value) == "Encountered a looping sdfRef: #/sdfProperty/bar"


def test_sdf_tm_unparsabable_sdf_ref():
    input = {
        "sdfProperty": {
            "foo": {"sdfRef": "bla/sdfProperty/bar"},
        },
    }

    expected_result = None

    with pytest.raises(Exception) as e_info:
        perform_conversion_test(input, expected_result)

    assert str(e_info.value) == "sdfRef bla/sdfProperty/bar could not be resolved"


def test_sdf_tm_failing_URL_sdf_ref():
    input = {
        "namespace": {"bla": "https://example.org"},
        "sdfProperty": {
            "foo": {"sdfRef": "bla:/sdfProperty/bar"},
        },
    }

    expected_result = None

    with pytest.raises(Exception) as e_info:
        perform_conversion_test(input, expected_result)

    error_message = "No valid SDF model could be retrieved from https://example.org"

    assert str(e_info.value) == error_message


def test_sdf_tm_succeeding_URL_sdf_ref():
    input = {
        "namespace": {
            "test": "https://raw.githubusercontent.com/one-data-model/playground/master/sdfObject/sdfobject-accelerometer.sdf.json"
        },
        "sdfProperty": {
            "foo": {"sdfRef": "test:/sdfObject/Accelerometer/sdfProperty/X_Value"},
        },
    }

    expected_result = {
        "@context": [
            "http://www.w3.org/ns/td",
            {
                "sdf": "https://example.com/sdf",
                "test": "https://raw.githubusercontent.com/one-data-model/playground/master/sdfObject/sdfobject-accelerometer.sdf.json",
            },
        ],
        "@type": "tm:ThingModel",
        "properties": {
            "foo": {
                "title": "X Value",
                "description": "The measured value along the X axis.",
                "readOnly": True,
                "type": "number",
                "sdf:jsonPointer": "#/sdfProperty/foo",
            },
        },
    }

    perform_conversion_test(input, expected_result)


def test_sdf_tm_sdf_choice():
    input = {
        "sdfProperty": {
            "foobar": {"sdfChoice": {"blah": {"type": "string"}}},
            "foobaz": {"enum": ["blargh"], "sdfChoice": {"blah": {"type": "string"}}},
        }
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "properties": {
            "foobar": {
                "enum": [{"sdf:choiceName": "blah", "type": "string"}],
                "sdf:jsonPointer": "#/sdfProperty/foobar",
            },
            "foobaz": {
                "enum": ["blargh", {"sdf:choiceName": "blah", "type": "string"}],
                "sdf:jsonPointer": "#/sdfProperty/foobaz",
            },
        },
    }

    perform_conversion_test(input, expected_result)


def test_sdf_tm_sdf_data_conversion():
    input = {
        "sdfData": {
            "fizz": {"type": "string"},
        },
        "sdfAction": {
            "foobar": {
                "label": "hi",
                "sdfInputData": {"sdfRef": "#/sdfData/fizz"},
            },
            "foobaz": {
                "label": "hi",
                "sdfInputData": {"sdfRef": "#/sdfAction/foobaz/sdfData/barfoo"},
                "sdfData": {"barfoo": {"sdfRef": "#/sdfData/fizz"}},
            },
        },
        "sdfEvent": {
            "foobar": {
                "label": "hi",
                "sdfOutputData": {"sdfRef": "#/sdfData/fizz"},
            },
            "foobaz": {
                "label": "hi",
                "sdfOutputData": {"sdfRef": "#/sdfEvent/foobaz/sdfData/barfoo"},
                "sdfData": {"barfoo": {"sdfRef": "#/sdfData/fizz"}},
            },
        },
    }

    expected_result = {
        "@context": ["http://www.w3.org/ns/td", {"sdf": "https://example.com/sdf"}],
        "@type": "tm:ThingModel",
        "schemaDefinitions": {
            "fizz": {
                "type": "string",
                "sdf:jsonPointer": "#/sdfData/fizz",
            },
            "foobaz_barfoo_action": {
                "sdf:jsonPointer": "#/sdfAction/foobaz/sdfData/barfoo",
                "tm:ref": "#/schemaDefinitions/fizz",
            },
            "foobaz_barfoo_event": {
                "sdf:jsonPointer": "#/sdfEvent/foobaz/sdfData/barfoo",
                "tm:ref": "#/schemaDefinitions/fizz",
            },
        },
        "actions": {
            "foobar": {
                "sdf:jsonPointer": "#/sdfAction/foobar",
                "input": {"tm:ref": "#/schemaDefinitions/fizz"},
                "title": "hi",
            },
            "foobaz": {
                "title": "hi",
                "input": {"tm:ref": "#/schemaDefinitions/foobaz_barfoo_action"},
                "sdf:jsonPointer": "#/sdfAction/foobaz",
            },
        },
        "events": {
            "foobar": {
                "sdf:jsonPointer": "#/sdfEvent/foobar",
                "data": {"tm:ref": "#/schemaDefinitions/fizz"},
                "title": "hi",
            },
            "foobaz": {
                "title": "hi",
                "data": {"tm:ref": "#/schemaDefinitions/foobaz_barfoo_event"},
                "sdf:jsonPointer": "#/sdfEvent/foobaz",
            },
        },
    }

    perform_conversion_test(input, expected_result)


def test_empty_namespace_conversion():
    input = {
        "namespace": {"cap": "https://example.com/capability/cap"},
        "defaultNamespace": "cap",
    }

    expected_result = {
        "@context": [
            "http://www.w3.org/ns/td",
            {
                "sdf": "https://example.com/sdf",
                "cap": "https://example.com/capability/cap",
            },
        ],
        "sdf:defaultNamespace": "cap",
        "@type": "tm:ThingModel",
    }

    perform_conversion_test(input, expected_result)
    perform_sdf_roundtrip_test(input)
