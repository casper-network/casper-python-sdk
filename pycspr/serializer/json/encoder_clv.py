from pycspr.crypto import checksummer
from pycspr.serializer.binary.encoder_clv import encode as clv_binary_encoder
from pycspr.serializer.json import encoder_clt
from pycspr.serializer.utils import cl_value_to_cl_type
from pycspr.serializer.utils import cl_value_to_parsed
from pycspr.types.cl import CLV_Value


def encode(entity: CLV_Value) -> dict:
    """Encoder: CL value -> JSON blob.

    :param entity: A CL value to be encoded.
    :returns: A JSON compatible dictionary.

    """
    return {
        "cl_type": encoder_clt.encode(
            cl_value_to_cl_type(entity)
        ),
        "bytes": checksummer.encode_bytes(
            clv_binary_encoder(entity)
        ),
        "parsed": cl_value_to_parsed(entity)
    }
