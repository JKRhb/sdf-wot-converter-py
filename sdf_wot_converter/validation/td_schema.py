td_schema = {
    "title": "Thing Description",
    "version": "1.1-28-January-2022",
    "description": "JSON Schema for validating TD instances against the TD information model. TD instances can be with or without terms that have default values",
    "$schema ": "http://json-schema.org/draft-07/schema#",
    "$id": "https://raw.githubusercontent.com/w3c/wot-thing-description/main/validation/td-json-schema-validation.json",
    "definitions": {
        "anyUri": {"type": "string", "format": "iri-reference"},
        "description": {"type": "string"},
        "descriptions": {"type": "object", "additionalProperties": {"type": "string"}},
        "title": {"type": "string"},
        "titles": {"type": "object", "additionalProperties": {"type": "string"}},
        "security": {
            "oneOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "scopes": {
            "oneOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "subprotocol": {"type": "string", "examples": ["longpoll", "websub", "sse"]},
        "thing-context-td-uri-v1": {
            "type": "string",
            "const": "https://www.w3.org/2019/wot/td/v1",
        },
        "thing-context-td-uri-v1.1": {
            "type": "string",
            "const": "https://www.w3.org/2022/wot/td/v1.1",
        },
        "thing-context-td-uri-temp": {
            "type": "string",
            "const": "http://www.w3.org/ns/td",
        },
        "thing-context": {
            "anyOf": [
                {
                    "$comment": "New context URI with other vocabularies after it but not the old one",
                    "type": "array",
                    "items": [{"$ref": "#/definitions/thing-context-td-uri-v1.1"}],
                    "additionalItems": {
                        "anyOf": [{"$ref": "#/definitions/anyUri"}, {"type": "object"}],
                        "not": {"$ref": "#/definitions/thing-context-td-uri-v1"},
                    },
                },
                {
                    "$comment": "Only the new context URI",
                    "$ref": "#/definitions/thing-context-td-uri-v1.1",
                },
                {
                    "$comment": "Old context URI, followed by the new one and possibly other vocabularies. minItems and contains are required since prefixItems does not say all items should be provided",
                    "type": "array",
                    "prefixItems": [
                        {"$ref": "#/definitions/thing-context-td-uri-v1"},
                        {"$ref": "#/definitions/thing-context-td-uri-v1.1"},
                    ],
                    "minItems": 2,
                    "contains": {"$ref": "#/definitions/thing-context-td-uri-v1.1"},
                    "additionalItems": {
                        "anyOf": [{"$ref": "#/definitions/anyUri"}, {"type": "object"}]
                    },
                },
            ]
        },
        "type_declaration": {
            "oneOf": [
                {"type": "string", "not": {"const": "tm:ThingModel"}},
                {
                    "type": "array",
                    "items": {"type": "string", "not": {"const": "tm:ThingModel"}},
                },
            ]
        },
        "dataSchema-type": {
            "type": "string",
            "enum": [
                "boolean",
                "integer",
                "number",
                "string",
                "object",
                "array",
                "null",
            ],
        },
        "dataSchema": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "title": {"$ref": "#/definitions/title"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "titles": {"$ref": "#/definitions/titles"},
                "writeOnly": {"type": "boolean"},
                "readOnly": {"type": "boolean"},
                "oneOf": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/dataSchema"},
                },
                "unit": {"type": "string"},
                "enum": {"type": "array", "minItems": 1, "uniqueItems": True},
                "format": {"type": "string"},
                "const": {},
                "default": {},
                "contentEncoding": {"type": "string"},
                "contentMediaType": {"type": "string"},
                "type": {"$ref": "#/definitions/dataSchema-type"},
                "items": {
                    "oneOf": [
                        {"$ref": "#/definitions/dataSchema"},
                        {
                            "type": "array",
                            "items": {"$ref": "#/definitions/dataSchema"},
                        },
                    ]
                },
                "maxItems": {"type": "integer", "minimum": 0},
                "minItems": {"type": "integer", "minimum": 0},
                "minimum": {"type": "number"},
                "maximum": {"type": "number"},
                "exclusiveMinimum": {"type": "number"},
                "exclusiveMaximum": {"type": "number"},
                "minLength": {"type": "integer", "minimum": 0},
                "maxLength": {"type": "integer", "minimum": 0},
                "multipleOf": {"$ref": "#/definitions/multipleOfDefinition"},
                "properties": {
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"}
                },
                "required": {"type": "array", "items": {"type": "string"}},
            },
        },
        "additionalResponsesDefinition": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "contentType": {"type": "string"},
                    "schema": {"type": "string"},
                    "success": {"type": "boolean"},
                },
            },
        },
        "multipleOfDefinition": {"type": ["integer", "number"], "exclusiveMinimum": 0},
        "expectedResponse": {
            "type": "object",
            "properties": {"contentType": {"type": "string"}},
        },
        "form_element_base": {
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}},
                    ]
                },
                "href": {"$ref": "#/definitions/anyUri"},
                "contentType": {"type": "string"},
                "contentCoding": {"type": "string"},
                "subprotocol": {"$ref": "#/definitions/subprotocol"},
                "security": {"$ref": "#/definitions/security"},
                "scopes": {"$ref": "#/definitions/scopes"},
                "response": {"$ref": "#/definitions/expectedResponse"},
                "additionalResponses": {
                    "$ref": "#/definitions/additionalResponsesDefinition"
                },
            },
            "required": ["href"],
            "additionalProperties": True,
        },
        "form_element_property": {
            "allOf": [{"$ref": "#/definitions/form_element_base"}],
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "enum": [
                                "readproperty",
                                "writeproperty",
                                "observeproperty",
                                "unobserveproperty",
                            ],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "readproperty",
                                    "writeproperty",
                                    "observeproperty",
                                    "unobserveproperty",
                                ],
                            },
                        },
                    ]
                }
            },
            "additionalProperties": True,
        },
        "form_element_action": {
            "allOf": [{"$ref": "#/definitions/form_element_base"}],
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "enum": ["invokeaction", "queryaction", "cancelaction"],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["invokeaction", "queryaction", "cancelaction"],
                            },
                        },
                    ]
                }
            },
            "additionalProperties": True,
        },
        "form_element_event": {
            "allOf": [{"$ref": "#/definitions/form_element_base"}],
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "enum": ["subscribeevent", "unsubscribeevent"],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["subscribeevent", "unsubscribeevent"],
                            },
                        },
                    ]
                }
            },
            "additionalProperties": True,
        },
        "form_element_root": {
            "allOf": [{"$ref": "#/definitions/form_element_base"}],
            "type": "object",
            "properties": {
                "op": {
                    "oneOf": [
                        {
                            "type": "string",
                            "enum": [
                                "readallproperties",
                                "writeallproperties",
                                "readmultipleproperties",
                                "writemultipleproperties",
                                "observeallproperties",
                                "unobserveallproperties",
                                "queryallactions",
                                "subscribeallevents",
                                "unsubscribeallevents",
                            ],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "readallproperties",
                                    "writeallproperties",
                                    "readmultipleproperties",
                                    "writemultipleproperties",
                                    "observeallproperties",
                                    "unobserveallproperties",
                                    "queryallactions",
                                    "subscribeallevents",
                                    "unsubscribeallevents",
                                ],
                            },
                        },
                    ]
                }
            },
            "additionalProperties": True,
        },
        "form": {
            "$comment": "This is NOT for validation purposes but for automatic generation of TS types. For more info, please see: https://github.com/w3c/wot-thing-description/pull/1319#issuecomment-994950057",
            "oneOf": [
                {"$ref": "#/definitions/form_element_property"},
                {"$ref": "#/definitions/form_element_action"},
                {"$ref": "#/definitions/form_element_event"},
                {"$ref": "#/definitions/form_element_root"},
            ],
        },
        "property_element": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "title": {"$ref": "#/definitions/title"},
                "titles": {"$ref": "#/definitions/titles"},
                "forms": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/definitions/form_element_property"},
                },
                "uriVariables": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"},
                },
                "observable": {"type": "boolean"},
                "writeOnly": {"type": "boolean"},
                "readOnly": {"type": "boolean"},
                "oneOf": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/dataSchema"},
                },
                "unit": {"type": "string"},
                "enum": {"type": "array", "minItems": 1, "uniqueItems": True},
                "format": {"type": "string"},
                "const": {},
                "default": {},
                "type": {"$ref": "#/definitions/dataSchema-type"},
                "items": {
                    "oneOf": [
                        {"$ref": "#/definitions/dataSchema"},
                        {
                            "type": "array",
                            "items": {"$ref": "#/definitions/dataSchema"},
                        },
                    ]
                },
                "maxItems": {"type": "integer", "minimum": 0},
                "minItems": {"type": "integer", "minimum": 0},
                "minimum": {"type": "number"},
                "maximum": {"type": "number"},
                "exclusiveMinimum": {"type": "number"},
                "exclusiveMaximum": {"type": "number"},
                "minLength": {"type": "integer", "minimum": 0},
                "maxLength": {"type": "integer", "minimum": 0},
                "multipleOf": {"$ref": "#/definitions/multipleOfDefinition"},
                "properties": {
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"}
                },
                "required": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["forms"],
            "additionalProperties": True,
        },
        "action_element": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "title": {"$ref": "#/definitions/title"},
                "titles": {"$ref": "#/definitions/titles"},
                "forms": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/definitions/form_element_action"},
                },
                "uriVariables": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"},
                },
                "input": {"$ref": "#/definitions/dataSchema"},
                "output": {"$ref": "#/definitions/dataSchema"},
                "safe": {"type": "boolean"},
                "idempotent": {"type": "boolean"},
            },
            "required": ["forms"],
            "additionalProperties": True,
        },
        "event_element": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "title": {"$ref": "#/definitions/title"},
                "titles": {"$ref": "#/definitions/titles"},
                "forms": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/definitions/form_element_event"},
                },
                "uriVariables": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/definitions/dataSchema"},
                },
                "subscription": {"$ref": "#/definitions/dataSchema"},
                "data": {"$ref": "#/definitions/dataSchema"},
                "dataResponse": {"$ref": "#/definitions/dataSchema"},
                "cancellation": {"$ref": "#/definitions/dataSchema"},
            },
            "required": ["forms"],
            "additionalProperties": True,
        },
        "base_link_element": {
            "type": "object",
            "properties": {
                "href": {"$ref": "#/definitions/anyUri"},
                "type": {"type": "string"},
                "rel": {"type": "string"},
                "anchor": {"$ref": "#/definitions/anyUri"},
            },
            "required": ["href"],
            "additionalProperties": True,
        },
        "link_element": {
            "allOf": [
                {"$ref": "#/definitions/base_link_element"},
                {
                    "not": {
                        "description": "A basic link element should not contain sizes",
                        "type": "object",
                        "properties": {"sizes": {}},
                        "required": ["sizes"],
                    }
                },
                {
                    "not": {
                        "description": "A basic link element should not contain icon or tm:extends",
                        "properties": {"rel": {"enum": ["icon", "tm:extends"]}},
                        "required": ["rel"],
                    }
                },
            ]
        },
        "icon_link_element": {
            "allOf": [
                {"$ref": "#/definitions/base_link_element"},
                {
                    "properties": {
                        "rel": {"const": "icon"},
                        "sizes": {"type": "string", "pattern": "[0-9]*x[0-9]+"},
                    },
                    "required": ["rel"],
                },
            ]
        },
        "noSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {"type": "string", "enum": ["nosec"]},
            },
            "required": ["scheme"],
        },
        "autoSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {"type": "string", "enum": ["auto"]},
            },
            "required": ["scheme"],
        },
        "comboSecurityScheme": {
            "oneOf": [
                {
                    "type": "object",
                    "properties": {
                        "@type": {"$ref": "#/definitions/type_declaration"},
                        "description": {"$ref": "#/definitions/description"},
                        "descriptions": {"$ref": "#/definitions/descriptions"},
                        "proxy": {"$ref": "#/definitions/anyUri"},
                        "scheme": {"type": "string", "enum": ["combo"]},
                        "oneOf": {
                            "type": "array",
                            "minItems": 2,
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["scheme", "oneOf"],
                },
                {
                    "type": "object",
                    "properties": {
                        "@type": {"$ref": "#/definitions/type_declaration"},
                        "description": {"$ref": "#/definitions/description"},
                        "descriptions": {"$ref": "#/definitions/descriptions"},
                        "proxy": {"$ref": "#/definitions/anyUri"},
                        "scheme": {"type": "string", "enum": ["combo"]},
                        "allOf": {
                            "type": "array",
                            "minItems": 2,
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["scheme", "allOf"],
                },
            ]
        },
        "basicSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {"type": "string", "enum": ["basic"]},
                "in": {
                    "type": "string",
                    "enum": ["header", "query", "body", "cookie", "auto"],
                },
                "name": {"type": "string"},
            },
            "required": ["scheme"],
        },
        "digestSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {"type": "string", "enum": ["digest"]},
                "qop": {"type": "string", "enum": ["auth", "auth-int"]},
                "in": {
                    "type": "string",
                    "enum": ["header", "query", "body", "cookie", "auto"],
                },
                "name": {"type": "string"},
            },
            "required": ["scheme"],
        },
        "apiKeySecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {"type": "string", "enum": ["apikey"]},
                "in": {"type": "string", "enum": ["header", "query", "body", "cookie"]},
                "name": {"type": "string"},
            },
            "required": ["scheme"],
        },
        "bearerSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {"type": "string", "enum": ["bearer"]},
                "authorization": {"$ref": "#/definitions/anyUri"},
                "alg": {"type": "string"},
                "format": {"type": "string"},
                "in": {
                    "type": "string",
                    "enum": ["header", "query", "body", "cookie", "auto"],
                },
                "name": {"type": "string"},
            },
            "required": ["scheme"],
        },
        "pskSecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {"type": "string", "enum": ["psk"]},
                "identity": {"type": "string"},
            },
            "required": ["scheme"],
        },
        "oAuth2SecurityScheme": {
            "type": "object",
            "properties": {
                "@type": {"$ref": "#/definitions/type_declaration"},
                "description": {"$ref": "#/definitions/description"},
                "descriptions": {"$ref": "#/definitions/descriptions"},
                "proxy": {"$ref": "#/definitions/anyUri"},
                "scheme": {"type": "string", "enum": ["oauth2"]},
                "authorization": {"$ref": "#/definitions/anyUri"},
                "token": {"$ref": "#/definitions/anyUri"},
                "refresh": {"$ref": "#/definitions/anyUri"},
                "scopes": {
                    "oneOf": [
                        {"type": "array", "items": {"type": "string"}},
                        {"type": "string"},
                    ]
                },
                "flow": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "string", "enum": ["code", "client", "device"]},
                    ]
                },
            },
            "required": ["scheme"],
        },
        "securityScheme": {
            "oneOf": [
                {"$ref": "#/definitions/noSecurityScheme"},
                {"$ref": "#/definitions/autoSecurityScheme"},
                {"$ref": "#/definitions/comboSecurityScheme"},
                {"$ref": "#/definitions/basicSecurityScheme"},
                {"$ref": "#/definitions/digestSecurityScheme"},
                {"$ref": "#/definitions/apiKeySecurityScheme"},
                {"$ref": "#/definitions/bearerSecurityScheme"},
                {"$ref": "#/definitions/pskSecurityScheme"},
                {"$ref": "#/definitions/oAuth2SecurityScheme"},
            ]
        },
    },
    "type": "object",
    "properties": {
        "id": {"type": "string", "format": "uri"},
        "title": {"$ref": "#/definitions/title"},
        "titles": {"$ref": "#/definitions/titles"},
        "properties": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/property_element"},
        },
        "actions": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/action_element"},
        },
        "events": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/event_element"},
        },
        "description": {"$ref": "#/definitions/description"},
        "descriptions": {"$ref": "#/definitions/descriptions"},
        "version": {
            "type": "object",
            "properties": {"instance": {"type": "string"}},
            "required": ["instance"],
        },
        "links": {
            "type": "array",
            "items": {
                "oneOf": [
                    {"$ref": "#/definitions/link_element"},
                    {"$ref": "#/definitions/icon_link_element"},
                ]
            },
        },
        "forms": {
            "type": "array",
            "minItems": 1,
            "items": {"$ref": "#/definitions/form_element_root"},
        },
        "base": {"$ref": "#/definitions/anyUri"},
        "securityDefinitions": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {"$ref": "#/definitions/securityScheme"},
        },
        "schemaDefinitions": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {"$ref": "#/definitions/dataSchema"},
        },
        "support": {"$ref": "#/definitions/anyUri"},
        "created": {"type": "string", "format": "date-time"},
        "modified": {"type": "string", "format": "date-time"},
        "profile": {
            "oneOf": [
                {"$ref": "#/definitions/anyUri"},
                {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/definitions/anyUri"},
                },
            ]
        },
        "security": {
            "oneOf": [
                {"type": "string"},
                {"type": "array", "minItems": 1, "items": {"type": "string"}},
            ]
        },
        "uriVariables": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/dataSchema"},
        },
        "@type": {"$ref": "#/definitions/type_declaration"},
        "@context": {"$ref": "#/definitions/thing-context"},
    },
    "required": ["title", "security", "securityDefinitions", "@context"],
    "additionalProperties": True,
}