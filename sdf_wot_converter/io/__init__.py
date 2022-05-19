import json
from typing import Callable, Dict, Optional
import urllib.request
import validators


def _load_model_from_path(input_path: str) -> Dict:  # pragma: no cover
    file = open(input_path)
    return json.load(file)


def _load_model_from_url(input_url: str) -> Dict:  # pragma: no cover
    with urllib.request.urlopen(input_url) as url:
        retrieved_model = json.loads(url.read().decode())
        return retrieved_model


def load_model(path_or_url: str) -> Dict:  # pragma: no cover
    if validators.url(path_or_url):
        return _load_model_from_url(path_or_url)
    else:
        return _load_model_from_path(path_or_url)


def save_model(output_path: str, model: Dict, indent=4):  # pragma: no cover
    file = open(output_path, "w")
    json.dump(model, file, indent=indent)


def load_and_save_model(
    input_path: str,
    output_path: str,
    indent=4,
):  # pragma: no cover
    model = load_model(input_path)
    save_model(output_path, model, indent=indent)


def load_optional_json_file(path: Optional[str]) -> Optional[Dict]:
    json_data = None
    if path:
        json_data = load_model(path)

    return json_data


def load_optional_json(json_string: Optional[str]) -> Optional[Dict]:
    json_data = None
    if json_string:
        json_data = json.loads(json_string)

    return json_data


def convert_model_from_path(
    from_path: str,
    to_path: str,
    converter_function: Callable,
    indent=4,
    **kwargs,
):  # pragma: no cover
    from_model = load_model(from_path)
    to_model = converter_function(from_model, **kwargs)
    save_model(to_path, to_model, indent=indent)


def convert_model_from_json(
    from_model_json: str,
    converter_function: Callable,
    indent=4,
    **kwargs,
):  # pragma: no cover
    from_model = json.loads(from_model_json)
    to_model = converter_function(from_model, **kwargs)
    return json.dumps(to_model, indent=indent)
