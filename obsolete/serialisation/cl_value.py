from pycspr.serialisation import cl_type
from pycspr.serialisation import cl_u8_array
from pycspr.serialisation import cl_value_parsed
from pycspr.types import CLValue


def from_bytes(value: bytes) -> CLValue:
    raise NotImplementedError()


def to_bytes(value: CLValue) -> bytes:
    return \
        cl_u8_array.to_bytes(cl_value_parsed.to_bytes(value)) + \
        cl_type.to_bytes(value.cl_type)


def from_json(value: dict) -> object:
    type_cl = cl_type.from_json(value["cl_type"])

    return CLValue(
        type_cl,
        cl_value_parsed.from_json(type_cl, value["parsed"]),
        bytes.fromhex(value["bytes"])
        )


def to_json(entity: CLValue) -> dict:
    return {
        "bytes": to_bytes(entity).hex(),
        "cl_type": cl_type.to_json(entity.cl_type),
        "parsed": cl_value_parsed.to_json(entity),
    }
