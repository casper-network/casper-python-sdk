from pycspr.serializer.binary import cl_type as cl_type_serialiser
from pycspr.serializer.binary import cl_value as cl_value_serialiser
from pycspr.serializer.binary import node_rpc as node_rpc_serialiser
from pycspr.types.cl import CLT_Type
from pycspr.types.cl import CLV_Value


def to_bytes(entity: object) -> bytes:
    if isinstance(entity, CLT_Type):
        return cl_type_serialiser.encode(entity)
    elif isinstance(entity, CLV_Value):
        return cl_value_serialiser.encode(entity)
    else:
        return node_rpc_serialiser.encode(entity)


def from_bytes(bstream: bytes, typedef: object = None) -> object:
    if isinstance(typedef, type(None)):
        return cl_type_serialiser.decode(bstream)
    elif isinstance(typedef, CLT_Type):
        return cl_value_serialiser.decode(bstream, typedef)
    else:
        return node_rpc_serialiser.decode(bstream, typedef)
