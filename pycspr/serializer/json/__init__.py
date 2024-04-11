import typing

from pycspr.serializer.json import cl_type as serializer_clt
from pycspr.serializer.json import cl_value as serializer_clv
from pycspr.serializer.json import crypto as serializer_crypto
from pycspr.serializer.json import node_rpc as serializer_node
from pycspr.types.cl import CLT_Type
from pycspr.types.cl import CLV_Value
from pycspr.types.cl.types import TYPESET as TYPESET_CLT
from pycspr.types.cl.values import TYPESET as TYPESET_CLV
from pycspr.types.crypto import TYPESET as TYPESET_CRYPTO
from pycspr.types.node import TYPESET as TYPESET_NODE


def to_json(entity: object) -> typing.Union[str, dict]:
    if isinstance(entity, CLT_Type):
        return serializer_clt.encode(entity)
    elif isinstance(entity, CLV_Value):
        return serializer_clv.encode(entity)
    else:
        return serializer_node.encode(entity)


def from_json(obj: dict, typedef: object = None) -> object:
    if isinstance(typedef, type(None)):
        return serializer_clt.decode(obj)
    # elif issubclass(typedef, CLV_Value):
    #     return serializer_clv.decode(obj)
    elif typedef in TYPESET_CLV:
        return serializer_clv.decode(obj)
    elif typedef in TYPESET_CRYPTO:
        return serializer_crypto.decode(typedef, obj)
    elif typedef in TYPESET_NODE:
        return serializer_node.decode(typedef, obj)
    else:
        raise ValueError("Unsupported type")
