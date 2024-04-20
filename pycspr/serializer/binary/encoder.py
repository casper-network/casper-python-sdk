from pycspr.serializer.binary import encoder_clt
from pycspr.serializer.binary import encoder_clv
from pycspr.serializer.binary import encoder_node
from pycspr.types.cl import CLT_Type
from pycspr.types.cl import CLV_Value
from pycspr.types.cl import TYPESET_CLT
from pycspr.types.node import TYPESET as TYPESET_NODE


def encode(entity: object) -> bytes:
    if isinstance(entity, CLT_Type):
        return encoder_clt.encode(entity)
    elif isinstance(entity, CLV_Value):
        return encoder_clv.encode(entity)
    else:
        return encoder_node.encode(entity)
