def from_bytes(value: bytes) -> bool:
    return bool(as_bytes[0])
    

def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_bytes(value: bool) -> bytes:
    return bytes([int(value)])


def to_json(value: object) -> dict:
    raise NotImplementedError()
