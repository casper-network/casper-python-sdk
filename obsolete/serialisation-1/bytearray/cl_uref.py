from pycspr.types import UnforgeableReference
from pycspr.serialisation.bytearray import cl_byte_array


def from_bytes(value: bytes) -> object:
    raise NotImplementedError()
    

def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_bytes(value: UnforgeableReference) -> bytes:
    return cl_byte_array.to_bytes(value.address + bytes([value.access_rights.value]))


def to_json(value: object) -> dict:
    raise NotImplementedError()
