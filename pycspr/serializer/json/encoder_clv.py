from pycspr.crypto import checksummer
from pycspr.serializer.binary.encoder_clv import encode as encode_clv
from pycspr.serializer.json.encoder_clt import encode as encode_clt
from pycspr.serializer.utils import clv_to_clt
from pycspr.serializer.utils import clv_to_parsed
from pycspr.type_defs.cl_values import CLV_Value


def encode(entity: CLV_Value) -> dict:
    """Encodes a domain entity instance to a JSON encodeable dictionary.

    :param entity: A CL value related type instance to be encoded.
    :returns: A JSON encodeable dictionary.

    """
    return {
        "cl_type": encode_clt(
            clv_to_clt(entity)
        ),
        "bytes": checksummer.encode_bytes(
            encode_clv(entity)
        ),
        "parsed": clv_to_parsed(entity)
    }
