import typing

import pycspr.factory.cl_type as cl_type_factory
from pycspr.crypto import KeyAlgorithm
from pycspr.types import CLAccessRights
from pycspr.types import CLType
from pycspr.types import CLValue
from pycspr.types import PublicKey
from pycspr.types import Key
from pycspr.types import KeyType
from pycspr.types import UnforgeableReference


# TODO
# ANY = 21
# MAP = 17
# RESULT = 16
# TUPLE_1 = 18
# TUPLE_2 = 19
# TUPLE_3 = 20


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


def key(value: bytes, key_type: typing.Union[KeyType, int]) -> CLValue:
    return CLValue(
        cl_type_factory.key(),
        Key(value, key_type)
        )


def key_from_string(value: str) -> CLValue:
    identifier = bytes.fromhex(value.split("-")[-1])
    if value.startswith("account-hash-"):        
        return key(identifier, KeyType.ACCOUNT)
    elif value.startswith("hash-"):
        return key(identifier, KeyType.HASH)
    elif value.startswith("uref-"):
        return key(identifier, KeyType.UREF)
    else:
        raise ValueError(f"Invalid key: {value}")


    return CLValue(
        cl_type_factory.key(key_type),
        Key(value, key_type)
        )


def list(inner_type: CLType, value: list) -> CLValue:
    return CLValue(
        cl_type_factory.list(inner_type),
        value
        )


def option(inner_type: CLType, value: object = None) -> CLValue:
    return CLValue(
        cl_type_factory.option(inner_type),
        value
        )


def public_key(value: typing.Union[bytes, PublicKey]) -> CLValue:
    if isinstance(value, bytes):
        value = PublicKey(KeyAlgorithm(value[0]), value[1:])

    return CLValue(
        cl_type_factory.public_key(),
        value
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
        UnforgeableReference(access_rights, address)
        )


def uref_from_string(value: str) -> CLValue:
    _, address, access_rights = value.split("-")

    return uref(bytes.fromhex(address), CLAccessRights(int(access_rights)))


def create(cl_type: CLType, parsed: object) -> CLValue:
    return CLValue(cl_type, parsed)
