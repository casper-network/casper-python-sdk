from pycspr.serializer.json.cl_type import decode as decode_cl_type
from pycspr.serializer.binary.cl_value import decode as decode_cl_value


def decode(encoded: dict):
    """Decoder: CL value <- JSON blob.

    :param encoded: A CL value encoded as a JSON compatible dictionary.
    :returns: A CL value.

    """
    assert "cl_type" in encoded and "bytes" in encoded

    # Set cl type to be decoded.
    cl_type = decode_cl_type(encoded["cl_type"])

    # Set byte stream to be decoded.
    bstream = encoded["bytes"]
    if isinstance(bstream, str):
        bstream = bytes.fromhex(bstream)

    # Decode cl value & assert that the entire byte stream has been consumed
    bstream, cl_value = decode_cl_value(bstream, cl_type)
    assert len(bstream) == 0

    return cl_value
