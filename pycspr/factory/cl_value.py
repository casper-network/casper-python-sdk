import typing

import pycspr.factory.cl_type as cl_type_factory
from pycspr.crypto import KeyAlgorithm
from pycspr.types import CLAccessRights
from pycspr.types import CLTypeKey
from pycspr.types import CLType
from pycspr.types import CLValue
from pycspr.types import PublicKey
from pycspr.types import StorageKey
from pycspr.types import StorageKeyType
from pycspr.types import UnforgeableReference


# TODO
# OPTION = 13
# RESULT = 16
# MAP = 17
# TUPLE_1 = 18
# TUPLE_2 = 19
# TUPLE_3 = 20
# ANY = 21


def boolean(value: bool) -> CLValue:
    cl_type = cl_type_factory.boolean()

    return CLValue(cl_type, value)


def byte_array(value: bytes) -> CLValue:
    cl_type = cl_type_factory.byte_array(len(value))

    return CLValue(cl_type, value)


def i32(value: int) -> CLValue:
    cl_type = cl_type_factory.i32()

    return CLValue(cl_type, value)


def i64(value: int) -> CLValue:
    cl_type = cl_type_factory.i64()

    return CLValue(cl_type, value)


def list(item_type: CLType, value: list) -> CLValue:
    cl_type = cl_type_factory.list(item_type)

    return CLValue(cl_type, value)


def public_key(value: typing.Union[bytes, PublicKey]) -> CLValue:
    cl_type = cl_type_factory.public_key()
    if isinstance(value, bytes):
        value = PublicKey(KeyAlgorithm(value[0]), value[1:])

    return CLValue(cl_type, value)


def storage_key(value: bytes, typeof: StorageKeyType) -> CLValue:    
    cl_type = cl_type_factory.key()
    value = StorageKey(value, typeof)

    return CLValue(cl_type, value)


def string(value: str) -> CLValue:
    cl_type = cl_type_factory.string()

    return CLValue(cl_type, value)


def u8(value: int) -> CLValue:
    cl_type = cl_type_factory.u8()

    return CLValue(cl_type, value)


def u32(value: int) -> CLValue:
    cl_type = cl_type_factory.u32()

    return CLValue(cl_type, value)


def u64(value: int) -> CLValue:
    cl_type = cl_type_factory.u64()

    return CLValue(cl_type, value)


def u128(value: int) -> CLValue:
    cl_type = cl_type_factory.u128()

    return CLValue(cl_type, value)


def u256(value: int) -> CLValue:
    cl_type = cl_type_factory.u256()

    return CLValue(cl_type, value)


def u512(value: int) -> CLValue:
    cl_type = cl_type_factory.u512()

    return CLValue(cl_type, value)


def unit() -> CLValue:
    cl_type = cl_type_factory.unit()

    return CLValue(cl_type, None)


def uref(address: bytes, access_rights: CLAccessRights) -> CLValue:
    cl_type = cl_type_factory.uref()
    value = UnforgeableReference(address, access_rights)

    return CLValue(cl_type, value)
