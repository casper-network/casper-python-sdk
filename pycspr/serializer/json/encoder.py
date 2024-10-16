import typing

from pycspr.serializer.json import encoder_clt, encoder_clv, encoder_crypto, encoder_node
from pycspr.types import TYPESET_CLT, TYPESET_CLV, TYPESET_NODE


def encode(entity: object) -> typing.Union[str, dict]:
    """Encodes a domain entity instance to a JSON encodeable dictionary.

    :param entity: A node related type instance to be encoded.
    :returns: A JSON encodeable dictionary or string.

    """
    typedef = type(entity)
    if typedef in TYPESET_CLT:
        return encoder_clt.encode(entity)
    elif typedef in TYPESET_CLV:
        return encoder_clv.encode(entity)
    elif typedef in TYPESET_NODE:
        return encoder_node.encode(entity)
    else:
        raise ValueError(f"Unsupported type: {typedef}")
