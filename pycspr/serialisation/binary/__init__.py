from pycspr.serialisation.binary import cl_type as cl_type_serialiser
from pycspr.serialisation.binary import cl_value as cl_value_serialiser
from pycspr.serialisation.binary import deploy as deploy_serialiser
from pycspr.types.cl_types import CL_Type
from pycspr.types.cl_values import CL_Value


def to_bytes(entity: object) -> bytes:
    if isinstance(entity, CL_Type):
        return cl_type_serialiser.encode(entity)
    elif isinstance(entity, CL_Value):
        return cl_value_serialiser.encode(entity)
    else:
        return deploy_serialiser.encode(entity)


def from_bytes(bstream: bytes, typedef: object = None) -> object:
    if isinstance(typedef, type(None)):
        return cl_type_serialiser.decode(bstream)
    elif isinstance(typedef, CL_Type):
        return cl_value_serialiser.decode(bstream, typedef)
    else:
        return deploy_serialiser.decode(bstream, typedef)
