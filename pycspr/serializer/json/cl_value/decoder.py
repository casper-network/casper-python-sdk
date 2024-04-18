from pycspr.types.cl import CLT_Type
from pycspr.serializer.json.cl_type import decode as decode_cl_type
from pycspr.serializer.binary.cl_value import decode as decode_cl_value


def decode(encoded: dict):
    """Decoder: CL value <- JSON blob.

    :param encoded: A CL value encoded as a JSON compatible dictionary.
    :returns: A CL value.

    """
    if "cl_type" not in encoded or "bytes" not in encoded:
        raise ValueError("Invalid CL value JSON encoding")

    # Set cl type.
    cl_typedef: CLT_Type = decode_cl_type(encoded["cl_type"])

    # Decode cl value.
    bstream, cl_value = decode_cl_value(
        cl_typedef,
        bytes.fromhex(encoded["bytes"])
        )

    # Assert entire byte stream has been consumed,
    assert len(bstream) == 0

    return cl_value
