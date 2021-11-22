def from_bytes(value: bytes) -> object:
    raise NotImplementedError()


def to_bytes(value: object) -> bytes:
    raise NotImplementedError()


def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_json(value: object) -> dict:
    raise NotImplementedError()
