from pycspr.codec import byte_array as byte_array_encoder
from pycspr.codec import json as json_encoder


_ENCODERS = {
    "byte-array": byte_array_encoder,
    "json": json_encoder,
}


def encode(entity: object, encoding: str = "json"):
    if encoding not in _ENCODERS:
        raise ValueError(f"Invalid encoding: {encoding}")

    return _ENCODERS[encoding].encode(entity)
