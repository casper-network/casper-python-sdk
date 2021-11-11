from pycspr.types import Key
from pycspr.types import KeyType


def from_bytes(value: bytes) -> Key:
    return Key(value[1:], KeyType(value[0]))
    

def to_bytes(value: Key) -> bytes:
    if value.key_type == KeyType.ACCOUNT:
        return bytes([0]) + value.identifier
    elif value.key_type == KeyType.HASH:
        return bytes([1]) + value.identifier
    elif value.key_type == KeyType.UREF:
        return bytes([2]) + value.identifier
    else:
        raise ValueError(f"Invalid key: {value}")


def from_json(value: str) -> Key:    
    identifier = bytes.fromhex(value.split("-")[-1])
    if value.startswith("account-hash-"):        
        return Key(identifier, KeyType.ACCOUNT)
    elif value.startswith("hash-"):
        return Key(identifier, KeyType.HASH)
    elif value.startswith("uref-"):
        return Key(identifier, KeyType.UREF)
    else:
        raise ValueError(f"Invalid key: {value}")


def to_json(value: Key) -> str:
    if value.key_type == KeyType.ACCOUNT:
        return f"account-hash-{value.identifier.hex()}"
    elif value.key_type == KeyType.HASH:
        return f"hash-{value.identifier.hex()}"
    elif value.key_type == KeyType.UREF:
        return f"uref-{value.identifier.hex()}"
    else:
        raise ValueError(f"Invalid key: {value}")
