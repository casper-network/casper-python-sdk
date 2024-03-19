import typing

from pycspr.serialisation.json import cl_type as serializer_of_cl_types
from pycspr.serialisation.json import cl_value as serializer_of_cl_values
from pycspr.serialisation.json import entity as serializer_of_entities
from pycspr.types.cl_types import CL_Type
from pycspr.types.cl_values import CL_Value


def to_json(entity: object) -> typing.Union[str, dict]:
    if isinstance(entity, CL_Type):
        return serializer_of_cl_types.encode(entity)
    elif isinstance(entity, CL_Value):
        return serializer_of_cl_values.encode(entity)
    else:
        return serializer_of_entities.encode(entity)


def from_json(obj: dict, typedef: object = None) -> object:
    if isinstance(typedef, type(None)):
        return serializer_of_cl_types.decode(obj)
    elif issubclass(typedef, CL_Value):
        return serializer_of_cl_values.decode(obj)
    else:
        return serializer_of_entities.decode(obj, typedef)
