from pycspr.serialisation.json.cl_type import decode as decode_cl_type
from pycspr.serialisation.binary.cl_value import decode as decode_cl_value


def decode(obj: dict):
    """Decoder: CL value <- JSON blob.

    :param obj: A CL value encoded as a JSON compatible dictionary.
    :returns: A CL value.

    """
    assert "cl_type" in obj and "bytes" in obj

    # Set cl type to be decoded.
    cl_type = decode_cl_type(obj["cl_type"])

    # Set byte stream to be decoded.
    bstream = obj["bytes"]
    if isinstance(bstream, str):
        bstream = bytes.fromhex(bstream)

    # Decode cl value & assert that the entire byte stream has been consumed
    bstream, cl_value = decode_cl_value(bstream, cl_type)
    assert len(bstream) == 0

    return cl_value
