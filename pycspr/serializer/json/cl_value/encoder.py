from pycspr.crypto import checksummer
from pycspr.serializer.binary.cl_value import encode as encode_cl_value
from pycspr.serializer.json.cl_type import encode as encode_cl_type
from pycspr.serializer.utils import cl_value_to_cl_type
from pycspr.serializer.utils import cl_value_to_parsed
from pycspr.types.cl import CLV_Value


def encode(entity: CLV_Value) -> dict:
    """Encoder: CL value -> JSON blob.

    :param entity: A CL value to be encoded.
    :returns: A JSON compatible dictionary.

    """
    return {
        "cl_type": encode_cl_type(cl_value_to_cl_type(entity)),
        "bytes": checksummer.encode_bytes(encode_cl_value(entity)),
        "parsed": cl_value_to_parsed(entity)
    }
