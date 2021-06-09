from pycspr.codec import json as json_encoder


_ENCODERS = {
    "json": json_encoder,
}


def encode(entity: object, encoding: str = 'json'):
    if encoding not in _ENCODERS:
        raise ValueError(f"Invalid encoding: {encoding}")

    return _ENCODERS[encoding].encode(entity)
