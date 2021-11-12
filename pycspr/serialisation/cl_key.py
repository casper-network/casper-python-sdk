from pycspr.types import StateKey
from pycspr.types import StateKeyType


def from_bytes(value: bytes) -> StateKey:
    return StateKey(value[1:], StateKeyType(value[0]))


def to_bytes(value: StateKey) -> bytes:
    if value.key_type == StateKeyType.ACCOUNT:
        return bytes([0]) + value.identifier
    elif value.key_type == StateKeyType.HASH:
        return bytes([1]) + value.identifier
    elif value.key_type == StateKeyType.UREF:
        return bytes([2]) + value.identifier
    else:
        raise ValueError(f"Invalid key: {value}")


def from_json(value: str) -> StateKey:
    identifier = bytes.fromhex(value.split("-")[-1])
    if value.startswith("account-hash-"):
        return StateKey(identifier, StateKeyType.ACCOUNT)
    elif value.startswith("hash-"):
        return StateKey(identifier, StateKeyType.HASH)
    elif value.startswith("uref-"):
        return StateKey(identifier, StateKeyType.UREF)
    else:
        raise ValueError(f"Invalid key: {value}")


def to_json(value: StateKey) -> str:
    if value.key_type == StateKeyType.ACCOUNT:
        return f"account-hash-{value.identifier.hex()}"
    elif value.key_type == StateKeyType.HASH:
        return f"hash-{value.identifier.hex()}"
    elif value.key_type == StateKeyType.UREF:
        return f"uref-{value.identifier.hex()}"
    else:
        raise ValueError(f"Invalid key: {value}")
