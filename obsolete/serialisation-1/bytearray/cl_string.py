from pycspr.serialisation.bytearray import cl_byte_array
from pycspr.serialisation.bytearray import cl_u32


def from_bytes(value: bytes) -> str:
    raise NotImplementedError()
    

def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_bytes(value: str) -> bytes:
    value = (value or "").encode("utf-8")
    value = cl_byte_array.to_bytes(value)

    return cl_u32.to_bytes(len(value)) + value


def to_json(value: object) -> dict:
    raise NotImplementedError()
