import typing

from pycspr.serialisation.binary import cl_type_binary_serialiser
from pycspr.serialisation.binary import cl_value_binary_serialiser
from pycspr.serialisation.binary import deploy_binary_serialiser
from pycspr.serialisation.json import cl_type_json_serialiser
from pycspr.serialisation.json import cl_value_json_serialiser
from pycspr.serialisation.json import deploy_json_serialiser
from pycspr.serialisation.utils.cl_value_to_cl_type import encode as cl_value_to_cl_type
from pycspr.serialisation.utils.cl_value_to_parsed import encode as cl_value_to_parsed
from pycspr.types.cl_types import CL_Type
from pycspr.types.cl_values import CL_Value


def to_bytes(entity: object) -> bytes:
    if isinstance(entity, CL_Type):
        serialiser = cl_type_binary_serialiser
    elif isinstance(entity, CL_Value):
        serialiser = cl_value_binary_serialiser
    else:
        serialiser = deploy_binary_serialiser

    return serialiser.encode(entity)


def to_json(entity: object) -> typing.Union[str, dict]:
    if isinstance(entity, CL_Type):
        serialiser = cl_type_json_serialiser
    elif isinstance(entity, CL_Value):
        serialiser = cl_value_json_serialiser
    else:
        serialiser = deploy_json_serialiser

    return serialiser.encode(entity)


def from_bytes(bstream: bytes, typedef: object = None) -> object:
    if isinstance(typedef, type(None)):
        return cl_type_binary_serialiser.decode(bstream)
    elif isinstance(typedef, CL_Type):
        return cl_value_binary_serialiser.decode(bstream, typedef)
    else:
        return deploy_binary_serialiser.decode(bstream, typedef)


def from_json(obj: dict, typedef: object = None) -> object:
    if isinstance(typedef, type(None)):
        return cl_type_json_serialiser.decode(obj)
    elif issubclass(typedef, CL_Value):
        return cl_value_json_serialiser.decode(obj)
    else:
        return deploy_json_serialiser.decode(obj, typedef)


__all__ = [
    "cl_value_to_cl_type",
    "to_bytes",
    "to_json",
    "from_bytes",
    "from_json",
]
