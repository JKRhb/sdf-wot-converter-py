sdf_framework_schema = {  # pragma: no cover
    "title": "sdf-framework.cddl",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$ref": "#/definitions/sdf-syntax",
    "definitions": {
        "sdf-syntax": {
            "type": "object",
            "properties": {
                "info": {"$ref": "#/definitions/sdfinfo"},
                "namespace": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                },
                "defaultNamespace": {"type": "string"},
                "sdfThing": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/thingqualities"},
                },
                "sdfProduct": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/productqualities"},
                },
                "sdfObject": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/objectqualities"},
                },
                "sdfProperty": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/propertyqualities"},
                },
                "sdfAction": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/actionqualities"},
                },
                "sdfEvent": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/eventqualities"},
                },
                "sdfData": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/dataqualities"},
                },
            },
            "additionalProperties": {},
        },
        "sdfinfo": {
            "type": "object",
            "required": ["title", "version", "copyright", "license"],
            "properties": {
                "title": {"type": "string"},
                "version": {"type": "string"},
                "copyright": {"type": "string"},
                "license": {"type": "string"},
            },
            "additionalProperties": {},
        },
        "thingqualities": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "label": {"type": "string"},
                "$comment": {"type": "string"},
                "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                "sdfRequired": {"$ref": "#/definitions/pointer-list"},
                "sdfObject": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/objectqualities"},
                },
                "sdfThing": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/thingqualities"},
                },
            },
            "additionalProperties": {},
        },
        "sdf-pointer": {"type": "string"},
        "pointer-list": {
            "type": "array",
            "items": {"$ref": "#/definitions/sdf-pointer"},
        },
        "objectqualities": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "label": {"type": "string"},
                "$comment": {"type": "string"},
                "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                "sdfRequired": {"$ref": "#/definitions/pointer-list"},
                "minItems": {"type": "number"},
                "maxItems": {"type": "number"},
                "sdfProperty": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/propertyqualities"},
                },
                "sdfAction": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/actionqualities"},
                },
                "sdfEvent": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/eventqualities"},
                },
                "sdfData": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/dataqualities"},
                },
            },
            "additionalProperties": {},
        },
        "propertyqualities": {"$ref": "#/definitions/dataqualities"},
        "dataqualities": {
            "anyOf": [
                {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["number", "string", "boolean", "integer", "array"],
                        },
                        "enum": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/allowed-types"},
                            "minItems": 1,
                        },
                        "const": {"$ref": "#/definitions/allowed-types"},
                        "default": {"$ref": "#/definitions/allowed-types"},
                        "minimum": {"type": "number"},
                        "maximum": {"type": "number"},
                        "exclusiveMinimum": {
                            "anyOf": [{"type": "boolean"}, {"type": "number"}]
                        },
                        "exclusiveMaximum": {
                            "anyOf": [{"type": "boolean"}, {"type": "number"}]
                        },
                        "multipleOf": {"type": "number"},
                        "minLength": {"type": "number"},
                        "maxLength": {"type": "number"},
                        "pattern": {"type": "string"},
                        "format": {
                            "anyOf": [
                                {"type": "string", "const": "date-time"},
                                {"type": "string", "const": "date"},
                                {"type": "string", "const": "time"},
                                {"type": "string", "const": "uri"},
                                {"type": "string", "const": "uri-reference"},
                                {"type": "string", "const": "uuid"},
                                {"type": "string"},
                            ]
                        },
                        "minItems": {"type": "number"},
                        "maxItems": {"type": "number"},
                        "uniqueItems": {"type": "boolean"},
                        "items": {
                            "anyOf": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": [
                                                "number",
                                                "string",
                                                "boolean",
                                                "integer",
                                            ],
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string", "const": "object"},
                                        "required": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "minItems": 1,
                                        },
                                        "properties": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "$ref": "#/definitions/dataqualities"
                                            },
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "sdfChoice": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "$ref": "#/definitions/dataqualities"
                                            },
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string"},
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                            ]
                        },
                        "description": {"type": "string"},
                        "label": {"type": "string"},
                        "$comment": {"type": "string"},
                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                        "sdfRequired": {"$ref": "#/definitions/pointer-list"},
                        "units": {"type": "string"},
                        "unit": {"type": "string"},
                        "scaleMinimum": {"type": "number"},
                        "scaleMaximum": {"type": "number"},
                        "observable": {"type": "boolean"},
                        "readable": {"type": "boolean"},
                        "writable": {"type": "boolean"},
                        "nullable": {"type": "boolean"},
                        "subtype": {
                            "anyOf": [
                                {"type": "string", "const": "byte-string"},
                                {"type": "string", "const": "unix-time"},
                                {"type": "string"},
                            ]
                        },
                        "sdfType": {
                            "anyOf": [
                                {"type": "string", "const": "byte-string"},
                                {"type": "string", "const": "unix-time"},
                                {"type": "string"},
                            ]
                        },
                        "contentFormat": {"type": "string"},
                    },
                    "additionalProperties": {},
                },
                {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "const": "object"},
                        "required": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        },
                        "properties": {
                            "type": "object",
                            "additionalProperties": {
                                "$ref": "#/definitions/dataqualities"
                            },
                        },
                        "enum": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/allowed-types"},
                            "minItems": 1,
                        },
                        "const": {"$ref": "#/definitions/allowed-types"},
                        "default": {"$ref": "#/definitions/allowed-types"},
                        "minimum": {"type": "number"},
                        "maximum": {"type": "number"},
                        "exclusiveMinimum": {
                            "anyOf": [{"type": "boolean"}, {"type": "number"}]
                        },
                        "exclusiveMaximum": {
                            "anyOf": [{"type": "boolean"}, {"type": "number"}]
                        },
                        "multipleOf": {"type": "number"},
                        "minLength": {"type": "number"},
                        "maxLength": {"type": "number"},
                        "pattern": {"type": "string"},
                        "format": {
                            "anyOf": [
                                {"type": "string", "const": "date-time"},
                                {"type": "string", "const": "date"},
                                {"type": "string", "const": "time"},
                                {"type": "string", "const": "uri"},
                                {"type": "string", "const": "uri-reference"},
                                {"type": "string", "const": "uuid"},
                                {"type": "string"},
                            ]
                        },
                        "minItems": {"type": "number"},
                        "maxItems": {"type": "number"},
                        "uniqueItems": {"type": "boolean"},
                        "items": {
                            "anyOf": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": [
                                                "number",
                                                "string",
                                                "boolean",
                                                "integer",
                                            ],
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string", "const": "object"},
                                        "required": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "minItems": 1,
                                        },
                                        "properties": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "$ref": "#/definitions/dataqualities"
                                            },
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "sdfChoice": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "$ref": "#/definitions/dataqualities"
                                            },
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string"},
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                            ]
                        },
                        "description": {"type": "string"},
                        "label": {"type": "string"},
                        "$comment": {"type": "string"},
                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                        "sdfRequired": {"$ref": "#/definitions/pointer-list"},
                        "units": {"type": "string"},
                        "unit": {"type": "string"},
                        "scaleMinimum": {"type": "number"},
                        "scaleMaximum": {"type": "number"},
                        "observable": {"type": "boolean"},
                        "readable": {"type": "boolean"},
                        "writable": {"type": "boolean"},
                        "nullable": {"type": "boolean"},
                        "subtype": {
                            "anyOf": [
                                {"type": "string", "const": "byte-string"},
                                {"type": "string", "const": "unix-time"},
                                {"type": "string"},
                            ]
                        },
                        "sdfType": {
                            "anyOf": [
                                {"type": "string", "const": "byte-string"},
                                {"type": "string", "const": "unix-time"},
                                {"type": "string"},
                            ]
                        },
                        "contentFormat": {"type": "string"},
                    },
                    "additionalProperties": {},
                },
                {
                    "type": "object",
                    "properties": {
                        "sdfChoice": {
                            "type": "object",
                            "additionalProperties": {
                                "$ref": "#/definitions/dataqualities"
                            },
                        },
                        "enum": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/allowed-types"},
                            "minItems": 1,
                        },
                        "const": {"$ref": "#/definitions/allowed-types"},
                        "default": {"$ref": "#/definitions/allowed-types"},
                        "minimum": {"type": "number"},
                        "maximum": {"type": "number"},
                        "exclusiveMinimum": {
                            "anyOf": [{"type": "boolean"}, {"type": "number"}]
                        },
                        "exclusiveMaximum": {
                            "anyOf": [{"type": "boolean"}, {"type": "number"}]
                        },
                        "multipleOf": {"type": "number"},
                        "minLength": {"type": "number"},
                        "maxLength": {"type": "number"},
                        "pattern": {"type": "string"},
                        "format": {
                            "anyOf": [
                                {"type": "string", "const": "date-time"},
                                {"type": "string", "const": "date"},
                                {"type": "string", "const": "time"},
                                {"type": "string", "const": "uri"},
                                {"type": "string", "const": "uri-reference"},
                                {"type": "string", "const": "uuid"},
                                {"type": "string"},
                            ]
                        },
                        "minItems": {"type": "number"},
                        "maxItems": {"type": "number"},
                        "uniqueItems": {"type": "boolean"},
                        "items": {
                            "anyOf": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": [
                                                "number",
                                                "string",
                                                "boolean",
                                                "integer",
                                            ],
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string", "const": "object"},
                                        "required": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "minItems": 1,
                                        },
                                        "properties": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "$ref": "#/definitions/dataqualities"
                                            },
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "sdfChoice": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "$ref": "#/definitions/dataqualities"
                                            },
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string"},
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                            ]
                        },
                        "description": {"type": "string"},
                        "label": {"type": "string"},
                        "$comment": {"type": "string"},
                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                        "sdfRequired": {"$ref": "#/definitions/pointer-list"},
                        "units": {"type": "string"},
                        "unit": {"type": "string"},
                        "scaleMinimum": {"type": "number"},
                        "scaleMaximum": {"type": "number"},
                        "observable": {"type": "boolean"},
                        "readable": {"type": "boolean"},
                        "writable": {"type": "boolean"},
                        "nullable": {"type": "boolean"},
                        "subtype": {
                            "anyOf": [
                                {"type": "string", "const": "byte-string"},
                                {"type": "string", "const": "unix-time"},
                                {"type": "string"},
                            ]
                        },
                        "sdfType": {
                            "anyOf": [
                                {"type": "string", "const": "byte-string"},
                                {"type": "string", "const": "unix-time"},
                                {"type": "string"},
                            ]
                        },
                        "contentFormat": {"type": "string"},
                    },
                    "additionalProperties": {},
                },
                {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "enum": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/allowed-types"},
                            "minItems": 1,
                        },
                        "const": {"$ref": "#/definitions/allowed-types"},
                        "default": {"$ref": "#/definitions/allowed-types"},
                        "minimum": {"type": "number"},
                        "maximum": {"type": "number"},
                        "exclusiveMinimum": {
                            "anyOf": [{"type": "boolean"}, {"type": "number"}]
                        },
                        "exclusiveMaximum": {
                            "anyOf": [{"type": "boolean"}, {"type": "number"}]
                        },
                        "multipleOf": {"type": "number"},
                        "minLength": {"type": "number"},
                        "maxLength": {"type": "number"},
                        "pattern": {"type": "string"},
                        "format": {
                            "anyOf": [
                                {"type": "string", "const": "date-time"},
                                {"type": "string", "const": "date"},
                                {"type": "string", "const": "time"},
                                {"type": "string", "const": "uri"},
                                {"type": "string", "const": "uri-reference"},
                                {"type": "string", "const": "uuid"},
                                {"type": "string"},
                            ]
                        },
                        "minItems": {"type": "number"},
                        "maxItems": {"type": "number"},
                        "uniqueItems": {"type": "boolean"},
                        "items": {
                            "anyOf": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": [
                                                "number",
                                                "string",
                                                "boolean",
                                                "integer",
                                            ],
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string", "const": "object"},
                                        "required": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "minItems": 1,
                                        },
                                        "properties": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "$ref": "#/definitions/dataqualities"
                                            },
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "sdfChoice": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "$ref": "#/definitions/dataqualities"
                                            },
                                        },
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string"},
                                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                                        "description": {"type": "string"},
                                        "$comment": {"type": "string"},
                                        "minimum": {"type": "number"},
                                        "maximum": {"type": "number"},
                                        "enum": {"type": "array", "minItems": 1},
                                        "format": {"type": "string"},
                                        "minLength": {"type": "number"},
                                        "maxLength": {"type": "number"},
                                    },
                                    "additionalProperties": {},
                                },
                            ]
                        },
                        "description": {"type": "string"},
                        "label": {"type": "string"},
                        "$comment": {"type": "string"},
                        "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                        "sdfRequired": {"$ref": "#/definitions/pointer-list"},
                        "units": {"type": "string"},
                        "unit": {"type": "string"},
                        "scaleMinimum": {"type": "number"},
                        "scaleMaximum": {"type": "number"},
                        "observable": {"type": "boolean"},
                        "readable": {"type": "boolean"},
                        "writable": {"type": "boolean"},
                        "nullable": {"type": "boolean"},
                        "subtype": {
                            "anyOf": [
                                {"type": "string", "const": "byte-string"},
                                {"type": "string", "const": "unix-time"},
                                {"type": "string"},
                            ]
                        },
                        "sdfType": {
                            "anyOf": [
                                {"type": "string", "const": "byte-string"},
                                {"type": "string", "const": "unix-time"},
                                {"type": "string"},
                            ]
                        },
                        "contentFormat": {"type": "string"},
                    },
                    "additionalProperties": {},
                },
            ]
        },
        "allowed-types": {
            "anyOf": [
                {"type": "number"},
                {"type": "string"},
                {"type": "boolean"},
                {"type": "null"},
                {"type": "array", "items": {"type": "number"}},
                {"type": "array", "items": {"type": "string"}},
                {"type": "array", "items": {"type": "boolean"}},
                {"type": "object", "additionalProperties": {}},
                {},
            ]
        },
        "actionqualities": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "label": {"type": "string"},
                "$comment": {"type": "string"},
                "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                "sdfRequired": {"$ref": "#/definitions/pointer-list"},
                "sdfInputData": {"$ref": "#/definitions/parameter-list"},
                "sdfRequiredInputData": {"$ref": "#/definitions/pointer-list"},
                "sdfOutputData": {"$ref": "#/definitions/parameter-list"},
                "sdfData": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/dataqualities"},
                },
            },
            "additionalProperties": {},
        },
        "parameter-list": {
            "anyOf": [
                {"$ref": "#/definitions/pointer-list"},
                {"$ref": "#/definitions/dataqualities"},
            ]
        },
        "eventqualities": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "label": {"type": "string"},
                "$comment": {"type": "string"},
                "sdfRef": {"$ref": "#/definitions/sdf-pointer"},
                "sdfRequired": {"$ref": "#/definitions/pointer-list"},
                "sdfOutputData": {"$ref": "#/definitions/parameter-list"},
                "sdfData": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/dataqualities"},
                },
            },
            "additionalProperties": {},
        },
        "productqualities": {"$ref": "#/definitions/thingqualities"},
    },
}
