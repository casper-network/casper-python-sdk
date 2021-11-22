from pycspr.serialisation.bytearray import cl_string
from pycspr.serialisation.bytearray import cl_u8_array
from pycspr.serialisation.bytearray import cl_type
from pycspr.serialisation.bytearray import cl_value
from pycspr.serialisation.bytearray import cl_value_parsed
from pycspr.types import DeployArgument


def from_bytes(value: bytes) -> DeployArgument:
    raise NotImplementedError()


def from_json(obj: dict) -> DeployArgument:
    return DeployArgument(
        name=obj[0],
        value=cl_value.from_json(obj[1])
        )


def to_bytes(entity: DeployArgument) -> bytes:
    return \
        cl_string.to_bytes(entity.name) + \
        cl_u8_array.to_bytes(
            cl_value_parsed.to_bytes(entity.value)
            ) + \
        cl_type.to_bytes(entity.value.cl_type)


def to_json(entity: DeployArgument) -> dict:
    return [
        entity.name,
        cl_value.to_json(entity.value)
    ]
