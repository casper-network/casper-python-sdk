import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.primitives.numeric import U32


def _decode_bool(bytes_in: bytes) -> typing.Tuple[bytes, bool]:
    assert len(bytes_in) >= 1
    return bytes_in[1:], bool(bytes_in[0])


def _decode_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    assert len(bytes_in) >= 4
    rem, size = decode(U32, bytes_in)
    assert len(rem) >= size
    return rem[size:], rem[:size]


def _decode_str(bytes_in: bytes) -> typing.Tuple[bytes, str]:
    assert len(bytes_in) >= 1
    rem, size = decode(U32, bytes_in)
    assert len(rem) >= size
    return rem[size:], rem[0:size].decode("utf-8")


# Simple types.
register_decoders({
    (bool, _decode_bool),
    (bytes, _decode_bytes),
    (str, _decode_str),
})
