def from_bytes(value: bytes) -> bytes:
    return value


def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_bytes(value: bytes) -> bytes:
    return bytes([]) if isinstance(value, type(None)) else value


def to_json(value: bytes) -> str:
    return value.hex()
