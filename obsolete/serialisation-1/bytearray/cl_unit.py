def from_bytes(value: bytes) -> None:
    raise NotImplementedError()
    

def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_bytes(value: type(None)) -> bytes:
    return bytes([])


def to_json(value: object) -> dict:
    raise NotImplementedError()
