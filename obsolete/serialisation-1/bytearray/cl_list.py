import typing

from pycspr.serialisation.bytearray import cl_vector


def from_bytes(value: bytes) -> object:
    raise NotImplementedError()


def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_bytes(value: list, inner_serialiser: typing.Callable) -> bytes:
    return cl_vector.to_bytes(list(map(inner_serialiser.to_bytes, value)))


def to_json(value: object) -> dict:
    raise NotImplementedError()
