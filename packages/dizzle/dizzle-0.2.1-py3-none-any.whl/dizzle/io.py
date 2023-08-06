import json
from typing import Union, Any, Dict, List


def read(path: str, **kwargs: Any) -> Union[str, bytes]:
    with open(path, **kwargs) as f:
        return f.read()


def write(path: str, payload: Union[str, bytes], mode: str = "w", **kwargs: Any) -> int:
    with open(path, mode=mode, **kwargs) as f:
        return f.write(payload)


def readj(path: str, **kwargs: Any) -> Union[Dict, List]:
    with open(path, **kwargs) as f:
        return json.load(f)


def writej(path: str, payload: Union[Dict, List], mode: str = "w", **kwargs: Any):
    with open(path, mode=mode, **kwargs) as f:
        json.dump(payload, f)
