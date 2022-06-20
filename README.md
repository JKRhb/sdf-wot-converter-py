[![Build Status](https://github.com/JKRhb/sdf-wot-converter-py/actions/workflows/build_status.yml/badge.svg)](https://github.com/JKRhb/sdf-wot-converter-py/actions/workflows/build_status.yml)
[![PyPI version](https://badge.fury.io/py/sdf-wot-converter.svg)](https://badge.fury.io/py/sdf-wot-converter)
[![codecov](https://codecov.io/gh/JKRhb/sdf-wot-converter-py/branch/main/graph/badge.svg?token=AWAN1GHKD8)](https://codecov.io/gh/JKRhb/sdf-wot-converter-py)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# SDF-WoT-Converter

This repository provides a Python-based converter from [SDF](https://datatracker.ietf.org/doc/html/draft-ietf-asdf-sdf) to [WoT TD](https://www.w3.org/TR/wot-thing-description/) including Thing Models.

The converter is both usable as a library and a command line tool. It provides
conversion functions between WoT Thing Descriptions, WoT Thing Models and SDF
Models (one for each combination). You can find a number of examples for the
usage of the converter down below as well as overviews for the conversion
between SDF and WoT TMs.

The CI pipeline is set up to automatically convert all (valid) models from the [oneDM playground](https://github.com/one-data-model/playground) to WoT Thing Models and upload to the results to [this repository](https://github.com/JKRhb/onedm-playground-wot-tm).

## Installation

You can install the converter using pip:

```sh
pip install sdf-wot-converter
```

Afterwards, it can be used both as a command line tool and a library.

## Using the command line tool

After installing the libary you should be able to call the converter in your terminal using `sdf-wot-converter` and one of the six available subcommands:

-   `sdf-to-tm`
-   `sdf-to-td`
-   `td-to-tm`
-   `td-to-sdf`
-   `tm-to-td`
-   `tm-to-sdf`

You can display available parameters by typing `sdf-wot-converter --help`.
A usage example for each subcommand can be found below.

### Examples

```bash
# Convert an SDF model to a WoT Thing Model
sdf-wot-converter sdf-to-tm -i examples/sdf/example.sdf.json -o converted-example.tm.jsonld

# Convert an SDF model to a WoT Thing Description
sdf-wot-converter sdf-to-td -i examples/sdf/example.sdf.json --mapping-files examples/sdf/example.sdf-mapping.json -o converted-example.td.jsonld

# Convert a WoT Thing Model to an SDF model
sdf-wot-converter tm-to-sdf -i examples/wot/example.tm.jsonld -o converted-example.sdf.json

# Convert a WoT Thing Model to a WoT Thing Description
sdf-wot-converter tm-to-td -i examples/wot/example-with-bindings.tm.jsonld -o converted-example.td.jsonld

# Convert a WoT Thing Description to an SDF model and a mapping file
sdf-wot-converter td-to-sdf -i examples/wot/example.td.jsonld -o converted-example.sdf.json --mapping-file-output converted-example.sdf-mapping.json

# Convert a WoT Thing Description to a WoT Thing Model
sdf-wot-converter td-to-tm -i examples/wot/example.td.jsonld -o converted-example.tm.jsonld
```

## Using the library

With the converter installed, you can use also use it as a library in your own projects. Below you can see examples for how to convert an SDF model to a WoT Thing Model and back again. As you can see, nested definitions from `sdfObject`s or `sdfThing`s are prefixed with the respective object or thing names.

```python
from sdf_wot_converter import (
    convert_sdf_to_wot_tm,
    convert_wot_tm_to_sdf,
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

thing_model = convert_sdf_to_wot_tm(sdf_model)

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
            "observable": False,
        }
    },
    "sdf:objectKey": "Switch",
}

assert thing_model == expected_thing_model

sdf_roundtrip_model = convert_wot_tm_to_sdf(thing_model)

assert sdf_model == sdf_roundtrip_model
```

## Mappings Overview

### SDF to WoT

Below you can find a mapping of the most important keywords of SDF to WoT.
We use Thing Models (TMs) as a reference here, as they are most similar to SDF
models.
When converting from SDF to WoT TD, the SDF model (and a mapping file which must
provide the necessary instance-specific information) is first converted to a TM,
which is in turn converted to a TD.

| SDF Keyword                 | WoT Class/Keyword                                                                          |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| sdfThing                    | TM with `tm:submodel` links                                                                |
| sdfObject                   | TM without `tm:submodel` links                                                             |
| sdfProperty                 | PropertyAffordance                                                                         |
| &nbsp;&nbsp;`writable`      | &nbsp;&nbsp;`readOnly` (negated)                                                           |
| &nbsp;&nbsp;`readable`      | &nbsp;&nbsp;`writeOnly` (negated)                                                          |
| sdfAction                   | ActionAffordance                                                                           |
| &nbsp;&nbsp;`sdfInputData`  | `input`                                                                                    |
| &nbsp;&nbsp;`sdfOutputData` | `output`                                                                                   |
| sdfEvent                    | EventAffordance                                                                            |
| &nbsp;&nbsp;`sdfOutputData` | `output`                                                                                   |
| sdfData                     | schemaDefinitions (at the Thing level)                                                     |
| `sdfRef`                    | `tm:ref`                                                                                   |
| `sdfChoice`                 | Enum of JSON objects with an (additional) `sdf:choiceName`                                 |
| `sdfRequired`               | `tm:required`                                                                              |
| `namespaces`                | `@context`                                                                                 |
| `defaultNamespace`          | `sdf:defaultNamespace`                                                                     |
| Info Block                  | _Multiple targets_                                                                         |
| &nbsp;&nbsp;`version`       | &nbsp;&nbsp;`model` field in the `Version` class                                           |
| &nbsp;&nbsp;`title`         | &nbsp;&nbsp;`sdf:title`                                                                    |
| &nbsp;&nbsp;`copyright`     | &nbsp;&nbsp;`sdf:copyright`                                                                |
| &nbsp;&nbsp;`license`       | &nbsp;&nbsp;link with relation-type `license` (if license value is a URL) or `sdf:license` |

### WoT to SDF

Below you can find a mapping of some of the most important classes and keywords from WoT to SDF. Note that there are still
some definitions missing in the table that are already covered by the converter implementation.

WoT TD definitions which are not covered by the core SDF vocabulary are mapped to a so-called SDF mapping file
(see [draft-bormann-asdf-sdf-mapping](https://datatracker.ietf.org/doc/html/draft-bormann-asdf-sdf-mapping)).

| WoT Class/Keyword               | SDF Keyword                                                                          |
| ------------------------------- | ------------------------------------------------------------------------------------ |
| Thing                           | sdfThing (if TM has `tm:submodel` links), sdfObject                                  |
| &nbsp;&nbsp;`title`             | &nbsp;&nbsp;`label`                                                                  |
| &nbsp;&nbsp;`description`       | &nbsp;&nbsp;`description`                                                            |
| &nbsp;&nbsp;`schemaDefinitions` | &nbsp;&nbsp;`sdfData`                                                                |
| &nbsp;&nbsp;`@context`          | `namespaces` of the SDF model (with exceptions)                                      |
| DataSchema                      | dataqualities                                                                        |
| &nbsp;&nbsp;`readOnly`          | Mapping File                                                                         |
| &nbsp;&nbsp;`writeOnly`         | Mapping File                                                                         |
| InteractionAffordance           | (Common Qualities)                                                                   |
| &nbsp;&nbsp;`title`             | &nbsp;&nbsp;`label`                                                                  |
| &nbsp;&nbsp;`description`       | &nbsp;&nbsp;`description`                                                            |
| PropertyAffordance              | sdfProperty                                                                          |
| &nbsp;&nbsp;`readOnly`          | &nbsp;&nbsp;`writable` (negated)                                                     |
| &nbsp;&nbsp;`writeOnly`         | &nbsp;&nbsp;`readable` (negated)                                                     |
| &nbsp;&nbsp;`observable`        | &nbsp;&nbsp;`observable` (negated)                                                   |
| ActionAffordance                | sdfAction                                                                            |
| &nbsp;&nbsp;`input`             | &nbsp;&nbsp;`sdfInputData`                                                           |
| &nbsp;&nbsp;`output`            | &nbsp;&nbsp;`sdfOutputData`                                                          |
| EventAffordance                 | sdfEvent                                                                             |
| &nbsp;&nbsp;`output`            | &nbsp;&nbsp;`sdfOutputData`                                                          |
| &nbsp;&nbsp;`subscription`      | Mapping File                                                                         |
| &nbsp;&nbsp;`cancellation`      | Mapping File                                                                         |
| &nbsp;&nbsp;`dataResponse`      | Mapping File                                                                         |
| `tm:ref`                        | `sdfRef`                                                                             |
| `tm:required`                   | `sdfRequired`                                                                        |
| Link                            | Mapping File, except for special link types (`license`, `tm:extends`, `tm:submodel`) |

## License

This project is licensed under the MIT license.

```
SPDX-License-Identifier: MIT
```
