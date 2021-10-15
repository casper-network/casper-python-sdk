import typing

from pycspr.serialisation.byte_array.constants import TypeTag_StorageKey
import pycspr.serialisation.byte_array.encoder.cl_primitive as primitives_encoder
from pycspr.types import PublicKey
from pycspr.types import StorageKey
from pycspr.types import StorageKeyType
from pycspr.types import UnforgeableReference


def encode_any(value: object) -> bytes:
    """Encodes a value of an unassigned type.

    """
    raise NotImplementedError()


def encode_list(value: list, inner_encoder: typing.Callable) -> bytes:
    """Encodes a list of values.

    """
    return encode_vector_of_t(list(map(inner_encoder, value)))


def encode_map(value: list) -> bytes:
    """Encodes a map of keys to associated values.

    """
    raise NotImplementedError()


def encode_option(value: object, inner_encoder: typing.Callable) -> bytes:
    """Encodes an optional CL value.

    """
    return bytes([0] if value is None else [1]) + inner_encoder(value)


def encode_public_key(value: PublicKey) -> bytes:
    """Encodes a public key.

    """
    return bytes([value.algo.value]) + value.pbk


def encode_result(value: object) -> bytes:
    """Encodes a smart contract execution result.

    """
    raise NotImplementedError()


def encode_storage_key(value: StorageKey) -> bytes:
    """Encodes a key mapped to data within global state.

    """
    _TYPE_TAGS = {
        StorageKeyType.ACCOUNT: TypeTag_StorageKey.Account,
        StorageKeyType.HASH: TypeTag_StorageKey.Hash,
        StorageKeyType.UREF: TypeTag_StorageKey.URef,
    }

    try:
        type_tag = _TYPE_TAGS[value.typeof]
    except KeyError:
        raise ValueError(f"Unencodeable key type: {value}")
    else:
        return bytes([type_tag.value]) + value.identifier


def encode_tuple1(value: tuple) -> bytes:
    """Encodes a 1-ary tuple of CL values.

    """
    raise NotImplementedError()


def encode_tuple2(value: tuple) -> bytes:
    """Encodes a 2-ary tuple of CL values.

    """
    raise NotImplementedError()


def encode_tuple3(value: tuple) -> bytes:
    """Encodes a 3-ary tuple of CL values.

    """
    raise NotImplementedError()


def encode_uref(value: UnforgeableReference):
    """Encodes an unforgeable reference.

    """
    return primitives_encoder.encode_byte_array(
        value.address + bytes([value.access_rights.value])
        )


def encode_vector_of_t(value: list):
    """Encodes an unbound vector.

    """
    return \
        primitives_encoder.encode_u32(len(value)) + \
        bytes([i for j in value for i in j])
