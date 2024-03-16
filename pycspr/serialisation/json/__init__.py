import typing

from pycspr.serialisation.json import cl_type as cl_type_serialiser
from pycspr.serialisation.json import cl_value as cl_value_serialiser
from pycspr.serialisation.json import deploy as deploy_serialiser
from pycspr.types.cl_types import CL_Type
from pycspr.types.cl_values import CL_Value


def to_json(entity: object) -> typing.Union[str, dict]:
    if isinstance(entity, CL_Type):
        return cl_type_serialiser.encode(entity)
    elif isinstance(entity, CL_Value):
        return cl_value_serialiser.encode(entity)
    else:
        return deploy_serialiser.encode(entity)


def from_json(obj: dict, typedef: object = None) -> object:
    if isinstance(typedef, type(None)):
        return cl_type_serialiser.decode(obj)
    elif issubclass(typedef, CL_Value):
        return cl_value_serialiser.decode(obj)
    else:
        return deploy_serialiser.decode(obj, typedef)
