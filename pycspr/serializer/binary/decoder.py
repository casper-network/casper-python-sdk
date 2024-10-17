from pycspr.serializer.binary import decoder_clt
from pycspr.serializer.binary import decoder_clv
from pycspr.serializer.binary import decoder_node
from pycspr.type_defs.cl_types import CLT_Type
from pycspr.types.cl import TYPESET_CLT
from pycspr.types.node import TYPESET as TYPESET_NODE


def decode(typedef: object, bstream: bytes) -> object:
    if isinstance(typedef, CLT_Type):
        return decoder_clv.decode(typedef, bstream)
    elif typedef in TYPESET_CLT:
        return decoder_clt.decode(bstream)
    elif typedef in TYPESET_NODE:
        return decoder_node.decode(typedef, bstream)
    else:
        raise ValueError("Unrecognized type definition")
