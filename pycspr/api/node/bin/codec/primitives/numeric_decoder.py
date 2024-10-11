import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.numeric import U8, U16, U32, U64, U128, U256, U512


def _decode_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    assert len(bytes_in) >= encoded_length
    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


def _decode_uint_big(bytes_in: bytes) -> typing.Tuple[bytes, int]:
    rem, size = decode(U8, bytes_in)
    rem, value = _decode_uint(rem, size)

    return rem, value


register_decoders({
    (U8, lambda x: _decode_uint(x, 1)),
    (U16, lambda x: _decode_uint(x, 2)),
    (U32, lambda x: _decode_uint(x, 4)),
    (U64, lambda x: _decode_uint(x, 8)),
    (U128, _decode_uint_big),
    (U256, _decode_uint_big),
    (U512, _decode_uint_big),
})
