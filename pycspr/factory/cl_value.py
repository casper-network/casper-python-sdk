import typing

import pycspr.factory.cl_type as cl_type_factory
from pycspr.crypto import KeyAlgorithm
from pycspr.types import CLAccessRights
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
    return CLValue(
        cl_type_factory.boolean(),
        value
        )


def byte_array(value: bytes) -> CLValue:
    return CLValue(
        cl_type_factory.byte_array(len(value)),
        value
        )


def i32(value: int) -> CLValue:
    return CLValue(
        cl_type_factory.i32(),
        value
        )


def i64(value: int) -> CLValue:
    return CLValue(
        cl_type_factory.i64(),
        value
        )


def list(item_type: CLType, value: list) -> CLValue:
    return CLValue(
        cl_type_factory.list(item_type),
        value
        )


def public_key(value: typing.Union[bytes, PublicKey]) -> CLValue:
    if isinstance(value, bytes):
        value = PublicKey(KeyAlgorithm(value[0]), value[1:])

    return CLValue(
        cl_type_factory.public_key(),
        value
        )


def storage_key(value: bytes, typeof: StorageKeyType) -> CLValue:
    return CLValue(
        cl_type_factory.key(),
        StorageKey(value, typeof)
        )


def string(value: str) -> CLValue:
    return CLValue(
        cl_type_factory.string(),
        value
        )


def u8(value: int) -> CLValue:
    return CLValue(
        cl_type_factory.u8(),
        value
        )


def u32(value: int) -> CLValue:
    return CLValue(
        cl_type_factory.u32(),
        value
        )


def u64(value: int) -> CLValue:
    return CLValue(
        cl_type_factory.u64(),
        value
        )


def u128(value: int) -> CLValue:
    return CLValue(
        cl_type_factory.u128(),
        value
        )


def u256(value: int) -> CLValue:
    return CLValue(
        cl_type_factory.u256(),
        value
        )


def u512(value: int) -> CLValue:
    return CLValue(
        cl_type_factory.u512(),
        value
        )


def unit() -> CLValue:
    return CLValue(
        cl_type_factory.unit(),
        None
        )


def uref(address: bytes, access_rights: CLAccessRights) -> CLValue:
    return CLValue(
        cl_type_factory.uref(),
        UnforgeableReference(address, access_rights)
        )


def create(value: object, cl_type: CLType) -> CLValue:
    return CLValue(cl_type, value)
