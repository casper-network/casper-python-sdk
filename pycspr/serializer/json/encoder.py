import typing

from pycspr.serializer.json import encoder_clt, encoder_clv, encoder_crypto, encoder_node
from pycspr.types import TYPESET_CLT, TYPESET_CLV, TYPESET_CRYPTO, TYPESET_NODE


def encode(entity: object) -> typing.Union[str, dict]:
    typedef = type(entity)
    if typedef in TYPESET_CLT:
        return encoder_clt.encode(entity)
    elif typedef in TYPESET_CLV:
        return encoder_clv.encode(entity)
    elif typedef in TYPESET_CRYPTO:
        return encoder_crypto.encode(entity)
    elif typedef in TYPESET_NODE:
        return encoder_node.encode(entity)
    else:
        raise ValueError(f"Unsupported type: {typedef}")
