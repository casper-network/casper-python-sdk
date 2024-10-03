import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.primitives.numeric import U8, U16, U32, U64, U128, U256, U512


def _decode_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    assert len(bytes_in) >= encoded_length
    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


def _decode_u512(bytes_in: bytes) -> typing.Tuple[bytes, int]:
    bytes_rem, size = decode(bytes_in, U8)
    bytes_rem, value = _decode_uint(bytes_rem, size)

    return bytes_rem, value


register_decoders({
    (U8, lambda x: _decode_uint(x, 1)),
    (U16, lambda x: _decode_uint(x, 2)),
    (U32, lambda x: _decode_uint(x, 4)),
    (U64, lambda x: _decode_uint(x, 8)),
    (U128, lambda x: NotImplementedError()),
    (U256, lambda x: NotImplementedError()),
    (U512, _decode_u512),
})
