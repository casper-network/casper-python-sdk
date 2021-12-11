from pycspr.serialisation.cl_type_from_json import decode as cl_type_from_json
from pycspr.serialisation.cl_value_from_bytes import decode as cl_value_from_bytes


def decode(encoded: dict):
    assert "cl_type" in encoded and "bytes" in encoded

    bstream = \
        bytes.fromhex(encoded["bytes"]) if isinstance(encoded["bytes"], str) else \
        encoded["bytes"]
    bstream, val = cl_value_from_bytes(bstream, cl_type_from_json(encoded["cl_type"]))
    
    # After decoding there should not be bytes left to decode.
    assert len(bstream) == 0

    return val
