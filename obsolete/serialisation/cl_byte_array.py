def from_bytes(value: bytes) -> bytes:
    return value


def to_bytes(value: bytes) -> bytes:
    return bytes([]) if isinstance(value, type(None)) else value


def from_json(value: str) -> bytes:
    return bytes.fromhex(value)


def to_json(value: bytes) -> str:
    return value.hex()
