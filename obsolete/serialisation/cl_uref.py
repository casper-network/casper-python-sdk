from pycspr.types import CL_URefAccessRights
from pycspr.types import UnforgeableReference
from pycspr.serialisation import cl_byte_array


def from_bytes(value: bytes) -> UnforgeableReference:
    return UnforgeableReference(
        CL_URefAccessRights(value[-1]),
        value[:-1]
    )


def to_bytes(value: UnforgeableReference) -> bytes:
    return cl_byte_array.to_bytes(value.address + bytes([value.access_rights.value]))


def from_json(value: str) -> UnforgeableReference:
    return from_string(value)


def to_json(value: UnforgeableReference) -> str:
    return to_string(value)


def from_string(value: str) -> UnforgeableReference:
    _, address, access_rights = value.split("-")
    return UnforgeableReference(
        CL_URefAccessRights(int(access_rights)),
        bytes.fromhex(address)
        )


def to_string(value: UnforgeableReference) -> str:
    return f"uref-{value.address.hex()}-{value.access_rights.value:03}"
