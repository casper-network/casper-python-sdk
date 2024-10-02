import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.primitives.crypto import DigestBytes
from pycspr.api.node.bin.types.primitives.numeric import U8, U16, U32, U64
from pycspr.api.node.bin.types.primitives.time import Timestamp


def decode_bool(bytes_in: bytes) -> typing.Tuple[bytes, bool]:
    assert len(bytes_in) >= 1

    return bytes_in[1:], bool(bytes_in[0])


def decode_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    assert len(bytes_in) >= 5

    bytes_rem, _ = decode(bytes_in, U32)

    return bytes_rem


def decode_digest_bytes(bytes_in: bytes, digest_length: int = 32) -> typing.Tuple[bytes, bytes]:
    assert len(bytes_in) >= digest_length

    return bytes_in[digest_length:], bytes_in[:digest_length]


def decode_str(bytes_in: bytes) -> typing.Tuple[bytes, str]:
    assert len(bytes_in) >= 1

    bytes_out, size = decode(bytes_in, U32)
    assert len(bytes_out) >= size

    return bytes_out[size:], bytes_out[0:size].decode("utf-8")


def decode_timestamp(bytes_in: bytes) -> typing.Tuple[bytes, Timestamp]:
    raise NotImplementedError()


def decode_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    assert len(bytes_in) >= encoded_length

    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


register_decoders({
    (bool, decode_bool),
    (bytes, decode_bytes),
    (str, decode_str),
    (DigestBytes, decode_digest_bytes),
    (Timestamp, decode_timestamp),
    (U8, lambda x: decode_uint(x, 1)),
    (U16, lambda x: decode_uint(x, 2)),
    (U32, lambda x: decode_uint(x, 4)),
    (U64, lambda x: decode_uint(x, 8)),
})
