from pycspr.serialisation.bytearray import cl_type
from pycspr.serialisation.bytearray import cl_u8_array
from pycspr.serialisation.bytearray import cl_value_parsed
from pycspr.types import CLValue


def from_bytes(value: bytes) -> CLValue:
    raise NotImplementedError()


def from_json(value: dict) -> object:
    cl_type = cl_type.from_json(value["cl_type"])
    as_bytes = bytes.fromhex(value["bytes"])
    if isinstance(cl_type, (CLType_Simple, CLType_ByteArray, CLType_Option)):
        parsed = byte_array_decoder(cl_type, as_bytes)
    else:
        parsed = None

    return CLValue(cl_type, parsed, as_bytes)


def to_bytes(value: CLValue) -> bytes:
    return \
        cl_u8_array.to_bytes(
            cl_value_parsed.to_bytes(value)
            ) + \
        cl_type.to_bytes(value.cl_type)


def to_json(entity: CLValue) -> dict:
    return {
        "bytes": to_bytes(entity).hex(),
        "cl_type": cl_type.to_json(entity.cl_type),
        "parsed": cl_value_parsed.to_json(entity),
    }
