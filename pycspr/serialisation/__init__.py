import typing

from pycspr.serialisation.binary import cl_type_binary_serialiser
from pycspr.serialisation.binary import cl_value_binary_serialiser
from pycspr.serialisation.binary import deploy_binary_serialiser
from pycspr.serialisation.json import cl_type_json_serialiser
from pycspr.serialisation.json import cl_value_json_serialiser
from pycspr.serialisation.json import deploy_json_serialiser
from pycspr.serialisation.utils import cl_value_to_cl_type
from pycspr.serialisation.utils import cl_value_to_parsed
from pycspr.types.cl_types import CL_Type
from pycspr.types.cl_values import CL_Value


def to_bytes(entity: object) -> bytes:
    if isinstance(entity, CL_Type):
        return cl_type_binary_serialiser.encode(entity)
    elif isinstance(entity, CL_Value):
        return cl_value_binary_serialiser.encode(entity)
    else:
        return deploy_binary_serialiser.encode(entity)


def to_json(entity: object) -> typing.Union[str, dict]:
    if isinstance(entity, CL_Type):
        return cl_type_json_serialiser.encode(entity)
    elif isinstance(entity, CL_Value):
        return cl_value_json_serialiser.encode(entity)
    else:
        return deploy_json_serialiser.encode(entity)


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
