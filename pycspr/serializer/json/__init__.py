import typing

from pycspr.serializer.json import cl_type as serializer_clt
from pycspr.serializer.json import cl_value as serializer_clv
from pycspr.serializer.json import crypto as serializer_crypto
from pycspr.serializer.json import node as serializer_node
from pycspr.serializer.json.crypto import DECODERS as DECODERS_CRYPTO
from pycspr.serializer.json.node import DECODERS as DECODERS_NODE
from pycspr.types import TYPESET_CLT
from pycspr.types import TYPESET_CLV
from pycspr.types import TYPESET_CRYPTO
from pycspr.types import TYPESET_NODE
from pycspr.types.cl import CLT_Type
from pycspr.types.cl import CLV_Value


def to_json(entity: object) -> typing.Union[str, dict]:
    typedef = type(entity)
    if typedef in TYPESET_CLT:
        return serializer_clt.encode(entity)
    elif typedef in TYPESET_CLV:
        return serializer_clv.encode(entity)
    elif typedef in TYPESET_CRYPTO:
        return serializer_crypto.encode(entity)
    elif typedef in TYPESET_NODE:
        return serializer_node.encode(entity)
    else:
        raise ValueError("Unsupported type")


def from_json(typedef: object, encoded: dict) -> object:
    if typedef in TYPESET_CLT:
        return serializer_clt.decode(encoded)
    elif typedef in TYPESET_CLV:
        return serializer_clv.decode(encoded)
    elif typedef in TYPESET_CRYPTO:
        return serializer_crypto.decode(typedef, encoded)
    elif typedef in TYPESET_NODE:
        return serializer_node.decode(typedef, encoded)
    else:
        raise ValueError("Unsupported type")
