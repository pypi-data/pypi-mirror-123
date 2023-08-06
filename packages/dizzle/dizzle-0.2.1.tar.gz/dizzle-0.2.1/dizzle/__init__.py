import json
from typing import Dict, Callable, Union, Any

from dizzle.geo import geocode_json


def to_snakecase(line: str) -> str:
    return "_".join(line.lower().split(" "))


def replacement(
    **kwargs: str,
) -> Callable[[str,], str]:
    def inner(line: str) -> str:
        for old, new in kwargs.items():
            line = line.replace(old, new)
        return line

    return inner


def pipeline(
    *fs: Callable[
        [
            str,
        ],
        str,
    ]
) -> Callable[[str,], str]:
    def inner(line: str) -> str:
        for f in fs:
            line = f(line)
        return line

    return inner


def normalize_keys(
    kwargs, normalizer=to_snakecase
) -> Union[Union[list[dict], dict], Any]:
    if isinstance(kwargs, list):
        return [normalize_keys(i, normalizer=normalizer) for i in kwargs]
    if isinstance(kwargs, dict):
        return {
            normalizer(k): normalize_keys(v, normalizer=normalizer)
            for k, v in kwargs.items()
        }
    return kwargs


def normalize_json_file(path: str, normalizer=to_snakecase) -> Dict:
    with open(path) as f:
        return normalize_keys(json.load(f), normalizer=normalizer)
