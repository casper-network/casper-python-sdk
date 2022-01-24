from pycspr.crypto import cl_checksum
from pycspr.serialisation.binary.cl_value import encode as encode_cl_value
from pycspr.serialisation.json.cl_type import encode as encode_cl_type
from pycspr.serialisation.utils import cl_value_to_cl_type
from pycspr.serialisation.utils import cl_value_to_parsed
from pycspr.types import cl_values


def encode(entity: cl_values.CL_Value) -> dict:
    """Encodes a CL value as a JSON compatible dictionary.

    :param entity: A CL value to be encoded.
    :returns: A JSON compatible dictionary.

    """
    return {
        "cl_type": encode_cl_type(cl_value_to_cl_type(entity)),
        "bytes": cl_checksum.encode(encode_cl_value(entity)),
        "parsed": cl_value_to_parsed(entity)
    }
