from pycspr.crypto import checksummer
from pycspr.serializer.binary.encoder_clv import encode as clv_binary_encoder
from pycspr.serializer.json import encoder_clt
from pycspr.serializer.utils import clv_to_clt
from pycspr.serializer.utils import clv_to_parsed
from pycspr.types.cl import CLV_Value


def encode(entity: CLV_Value) -> dict:
    """Encodes a domain entity instance to a JSON encodeable dictionary.

    :param entity: A CL value related type instance to be encoded.
    :returns: A JSON encodeable dictionary.

    """
    return {
        "cl_type": encoder_clt.encode(
            clv_to_clt(entity)
        ),
        "bytes": checksummer.encode_bytes(
            clv_binary_encoder(entity)
        ),
        "parsed": clv_to_parsed(entity)
    }
