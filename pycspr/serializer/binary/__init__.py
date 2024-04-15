from pycspr.serializer.binary import cl_type as serializer_clt
from pycspr.serializer.binary import cl_value as serializer_clv
from pycspr.serializer.binary import node as serializer_node
from pycspr.types.cl import CLT_Type
from pycspr.types.cl import CLV_Value
from pycspr.types.cl import TYPESET_CLT
from pycspr.types.node import TYPESET as TYPESET_NODE


def to_bytes(entity: object) -> bytes:
    if isinstance(entity, CLT_Type):
        return serializer_clt.encode(entity)
    elif isinstance(entity, CLV_Value):
        return serializer_clv.encode(entity)
    else:
        return serializer_node.encode(entity)


def from_bytes(typedef: object, bstream: bytes) -> object:
    if isinstance(typedef, CLT_Type):
        return serializer_clv.decode(typedef, bstream)
    elif typedef in TYPESET_CLT:
        return serializer_clt.decode(bstream)
    elif typedef in TYPESET_NODE:
        return serializer_node.decode(typedef, bstream)
    else:
        raise ValueError("Unrecognized type definition")
