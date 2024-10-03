import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.primitives.crypto import DigestBytes, KeyAlgorithm, PublicKeyBytes
from pycspr.api.node.bin.types.primitives.numeric import U8, U16, U32, U64
from pycspr.api.node.bin.types.primitives.time import Timestamp


def decode_crypto_digest_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    assert len(bytes_in) >= 32
    return bytes_in[32:], bytes_in[:32]


def decode_crypto_key_algo(bytes_in: bytes) -> typing.Tuple[bytes, KeyAlgorithm]:
    assert len(bytes_in) >= 1
    bytes_rem, algo_type = decode(bytes_in, U8)
    return bytes_rem, KeyAlgorithm(algo_type)


def decode_crypto_public_key_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    bytes_rem, key_algo = decode(bytes_in, KeyAlgorithm)
    if key_algo == KeyAlgorithm.ED25519:
        return bytes_rem[32:], bytes_rem[:32]
    elif key_algo == KeyAlgorithm.ED25519:
        return bytes_rem[33:], bytes_rem[:33]
    elif key_algo == KeyAlgorithm.SYSTEM:
        return bytes_rem, bytes([])
    else:
        raise ValueError("Invalid ECC key algo type")


def decode_numeric_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    assert len(bytes_in) >= encoded_length
    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


def decode_simple_bool(bytes_in: bytes) -> typing.Tuple[bytes, bool]:
    assert len(bytes_in) >= 1
    return bytes_in[1:], bool(bytes_in[0])


def decode_simple_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    assert len(bytes_in) >= 5
    bytes_rem, _ = decode(bytes_in, U32)
    return bytes_rem


def decode_simple_str(bytes_in: bytes) -> typing.Tuple[bytes, str]:
    assert len(bytes_in) >= 1
    bytes_out, size = decode(bytes_in, U32)
    assert len(bytes_out) >= size
    return bytes_out[size:], bytes_out[0:size].decode("utf-8")


def decode_time_timestamp(bytes_in: bytes) -> typing.Tuple[bytes, Timestamp]:
    assert len(bytes_in) >= 4
    bytes_out, ts_ms = decode(bytes_in, U64)
    return bytes_out, Timestamp(float(ts_ms))


# Simple types.
register_decoders({
    (bool, decode_simple_bool),
    (bytes, decode_simple_bytes),
    (str, decode_simple_str),
})

# Numeric types.
register_decoders({
    (U8, lambda x: decode_numeric_uint(x, 1)),
    (U16, lambda x: decode_numeric_uint(x, 2)),
    (U32, lambda x: decode_numeric_uint(x, 4)),
    (U64, lambda x: decode_numeric_uint(x, 8)),
})

# Crypto types.
register_decoders({
    (DigestBytes, decode_crypto_digest_bytes),
    (KeyAlgorithm, decode_crypto_key_algo),
    (PublicKeyBytes, decode_crypto_public_key_bytes),
    (Timestamp, decode_time_timestamp),
})
