from pycspr.types import StateKey
from pycspr.types import StateKeyType


def from_bytes(value: bytes) -> object:
    raise NotImplementedError()
    

def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_bytes(value: StateKey) -> bytes:
    if value.key_type == StateKeyType.ACCOUNT:
        return bytes([0]) + value.identifier
    elif value.key_type == StateKeyType.HASH:
        return bytes([1]) + value.identifier
    elif value.key_type == StateKeyType.UREF:
        return bytes([2]) + value.identifier
    else:
        raise ValueError(f"Unencodeable key type: {value}")


def to_json(value: object) -> dict:
    raise NotImplementedError()
