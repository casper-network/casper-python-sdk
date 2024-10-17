from pycspr.type_defs.cl_types import CLT_Type
from pycspr.serializer.json.decoder_clt import decode as decode_clt
from pycspr.serializer.binary.decoder_clv import decode as decode_clv


def decode(encoded: dict):
    """Decodes a domain entity instance from JSON encoded data.

    :param encoded: JSON encoded data.
    :returns: A CL value related type instance.

    """
    if "cl_type" not in encoded or "bytes" not in encoded:
        raise ValueError("Invalid CL value JSON encoding")

    # Set cl type.
    cl_typedef: CLT_Type = decode_clt(encoded["cl_type"])

    # Decode cl value.
    bstream, cl_value = decode_clv(
        cl_typedef,
        bytes.fromhex(encoded["bytes"])
        )

    # Assert entire byte stream has been consumed,
    assert len(bstream) == 0

    return cl_value
