from pycspr.serialisation.cl_type_from_json import decode as cl_type_from_json
from pycspr.serialisation.cl_value_from_bytes import decode as cl_value_from_bytes


def decode(obj: dict):
    """Decodes a CL value from a JSON object.

    :param obj: A CL value encoded as a JSON compatible dictionary.
    :returns: A CL value.

    """
    assert "cl_type" in obj and "bytes" in obj
    cl_type = cl_type_from_json(obj["cl_type"])
    bstream = obj["bytes"]
    if isinstance(bstream, str):
        bstream = bytes.fromhex(bstream)

    bstream, cl_value = cl_value_from_bytes(bstream, cl_type)
    assert len(bstream) == 0

    return cl_value
