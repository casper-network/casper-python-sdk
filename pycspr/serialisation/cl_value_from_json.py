from pycspr.serialisation.cl_type_from_json import decode as cl_type_from_json
from pycspr.serialisation.cl_value_from_bytes import decode as cl_value_from_bytes
from pycspr.types.cl import cl_types


def decode(encoded: dict):
    assert "cl_type" in encoded and "bytes" in encoded

    return cl_value_from_bytes(
        bytes.fromhex(encoded["bytes"]) if isinstance(encoded["bytes"], str) else encoded["bytes"],
        cl_type_from_json(encoded["cl_type"])
        )
