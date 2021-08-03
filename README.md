[![Build Status](https://github.com/JKRhb/sdf-wot-converter-py/actions/workflows/build_status.yml/badge.svg)](https://github.com/JKRhb/sdf-wot-converter-py/actions/workflows/build_status.yml)
[![codecov](https://codecov.io/gh/JKRhb/sdf-wot-converter-py/branch/main/graph/badge.svg?token=AWAN1GHKD8)](https://codecov.io/gh/JKRhb/sdf-wot-converter-py)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# SDF-WoT-Converter (Python Edition)

This repository provides a Python-based converter from [SDF](https://datatracker.ietf.org/doc/html/draft-ietf-asdf-sdf-05) to [WoT TD](https://www.w3.org/TR/wot-thing-description/) including Thing Models.

The converter is both usable as a library and a command line tool. It is based on my [Rust implementation](https://github.com/JKRhb/sdf-wot-converter) but is (when it comes to the conversion from SDF to Thing Models) already more mature as development in Python turned out to be much faster. The final version of this converter, however, will be reimplemented in Rust once it is finished to also support more constrained environments.

The CI pipeline is set up to automatically convert all (valid) models from the [oneDM playground](https://github.com/one-data-model/playground) to WoT Thing Models and upload to the results to [this repository](https://github.com/JKRhb/onedm-playground-wot-tm).

## Installation

After cloning the repository run the following commands in the repo's directory:

```sh
pip install -q build
python -m build
pip install --find-links dist/ sdf-wot-converter
```

You need at least Python 3.6 and pip installed.

## Using the command line tool

After installing the libary you should be able to call the converter in your terminal using `sdf-wot-converter`. You can display available parameters by typing  `sdf-wot-converter --help`. So far, you can only convert from SDF to WoT Thing models but the other direction will be added soon.

### Example

```bash
# Convert an SDF model to a WoT Thing Model
sdf-wot-converter --from-sdf examples/sdf/example.sdf.json --to-tm converted-example.tm.json
```

## License

This project is licensed under the MIT license.

```
SPDX-License-Identifier: MIT
```
