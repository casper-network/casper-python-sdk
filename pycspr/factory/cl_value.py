import typing

from pycspr.crypto import KeyAlgorithm
from pycspr.factory import cl_type as create_cl_type
from pycspr.factory.accounts import create_public_key_from_account_key
from pycspr.types import CLAccessRights
from pycspr.types import CLType
from pycspr.types import CLValue
from pycspr.types import StateKey
from pycspr.types import StateKeyType
from pycspr.types import PublicKey
from pycspr.types import UnforgeableReference


def any(value: object) -> CLValue:
    raise NotImplementedError()


def boolean(value: bool) -> CLValue:
    return CLValue(
        create_cl_type.boolean(),
        value
        )

def byte_array(value: bytes) -> CLValue:
    return CLValue(
        create_cl_type.byte_array(len(value)),
        value
        )


def i32(value: int) -> CLValue:
    return CLValue(
        create_cl_type.i32(),
        value
        )


def i64(value: int) -> CLValue:
    return CLValue(
        create_cl_type.i64(),
        value
        )


def key(value: bytes, key_type: typing.Union[StateKeyType, int]) -> CLValue:
    return CLValue(
        create_cl_type.key(),
        StateKey(value, key_type)
        )


def key_from_string(value: str) -> CLValue:
    identifier = bytes.fromhex(value.split("-")[-1])
    if value.startswith("account-hash-"):
        return key(identifier, StateKeyType.ACCOUNT)
    elif value.startswith("hash-"):
        return key(identifier, StateKeyType.HASH)
    elif value.startswith("uref-"):
        return key(identifier, StateKeyType.UREF)
    else:
        raise ValueError(f"Invalid key: {value}")


def list(inner_type: CLType, value: list) -> CLValue:
    return CLValue(
        create_cl_type.list(inner_type),
        value
        )


def map(value: dict) -> CLValue:
    raise NotImplementedError()


def option(inner_type: CLType, value: object = None) -> CLValue:
    return CLValue(
        create_cl_type.option(inner_type),
        value
        )


def public_key(value: typing.Union[bytes, PublicKey]) -> CLValue:
    if isinstance(value, bytes):
        value = create_public_key_from_account_key(value)
        value = PublicKey(KeyAlgorithm(value[0]), value[1:])

    return CLValue(
        create_cl_type.public_key(),
        value
        )


def result() -> CLValue:
    raise NotImplementedError()


def string(value: str) -> CLValue:
    return CLValue(
        create_cl_type.string(),
        value
        )


def tuple_1(item_1: CLValue) -> CLValue:
    raise NotImplementedError()


def tuple_2(item_1: CLValue, item_2: CLValue) -> CLValue:
    raise NotImplementedError()


def tuple_3(item_1: CLValue, item_2: CLValue, item_3: CLValue) -> CLValue:
    raise NotImplementedError()


def u8(value: int) -> CLValue:
    return CLValue(
        create_cl_type.u8(),
        value
        )


def u32(value: int) -> CLValue:
    return CLValue(
        create_cl_type.u32(),
        value
        )


def u64(value: int) -> CLValue:
    return CLValue(
        create_cl_type.u64(),
        value
        )


def u128(value: int) -> CLValue:
    return CLValue(
        create_cl_type.u128(),
        value
        )


def u256(value: int) -> CLValue:
    return CLValue(
        create_cl_type.u256(),
        value
        )


def u512(value: int) -> CLValue:
    return CLValue(
        create_cl_type.u512(),
        value
        )


def unit() -> CLValue:
    return CLValue(
        create_cl_type.unit(),
        None
        )


def uref(address: bytes, access_rights: CLAccessRights) -> CLValue:
    return CLValue(
        create_cl_type.uref(),
        UnforgeableReference(access_rights, address)
        )


def uref_from_string(value: str) -> CLValue:
    _, address, access_rights = value.split("-")

    return uref(bytes.fromhex(address), CLAccessRights(int(access_rights)))
