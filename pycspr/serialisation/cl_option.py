import typing


def from_bytes(value: bytes) -> object:
    raise NotImplementedError()


def to_bytes(value: object, inner_serialiser: typing.Callable) -> bytes:
    return bytes([0] if value is None else [1]) + inner_serialiser.to_bytes(value)


def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_json(value: object) -> dict:
    raise NotImplementedError()
