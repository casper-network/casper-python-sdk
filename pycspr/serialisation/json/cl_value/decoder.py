from pycspr.serialisation.json.cl_type import decode as decode_cl_type
from pycspr.serialisation.binary.cl_value import decode as decode_cl_value


def decode(obj: dict):
    """Decodes a CL value from a JSON object.

    :param obj: A CL value encoded as a JSON compatible dictionary.
    :returns: A CL value.

    """
    assert "cl_type" in obj and "bytes" in obj
    cl_type = decode_cl_type(obj["cl_type"])
    bstream = obj["bytes"]
    if isinstance(bstream, str):
        bstream = bytes.fromhex(bstream)

    bstream, cl_value = decode_cl_value(bstream, cl_type)
    assert len(bstream) == 0

    return cl_value
