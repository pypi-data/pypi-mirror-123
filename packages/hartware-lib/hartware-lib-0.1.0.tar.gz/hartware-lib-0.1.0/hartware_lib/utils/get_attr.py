from typing import Any, Dict


def get_or_raise(data: Dict, key: str, error_msg: str) -> Any:
    value = data.get(key)

    assert value, error_msg

    return value
