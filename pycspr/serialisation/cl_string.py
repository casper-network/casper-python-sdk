from pycspr.serialisation import cl_byte_array
from pycspr.serialisation import cl_u32


def from_bytes(value: bytes) -> str:
    return value[cl_u32.BYTE_LENGTH:].decode("utf-8")
    

def to_bytes(value: str) -> bytes:
    value = (value or "").encode("utf-8")
    value = cl_byte_array.to_bytes(value)

    return cl_u32.to_bytes(len(value)) + value


def from_json(value: str) -> str:
    return value


def to_json(value: str) -> str:
    return value
