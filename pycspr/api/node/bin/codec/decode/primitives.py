import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.type_defs.primitives import \
    U8, U16, U32, U64, U128, U256, U512, \
    TimeDifference, Timestamp


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


def _decode_time_difference(bytes_in: bytes) -> typing.Tuple[bytes, TimeDifference]:
    assert len(bytes_in) >= 4
    rem, timediff_ms = decode(U64, bytes_in)
    return rem, Timestamp(timediff_ms)


def _decode_time_timestamp(bytes_in: bytes) -> typing.Tuple[bytes, Timestamp]:
    assert len(bytes_in) >= 4
    rem, ts_ms = decode(U64, bytes_in)
    return rem, Timestamp(float(ts_ms))


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
    (bool, _decode_bool),
    (bytes, _decode_bytes),
    (str, _decode_str),
    (TimeDifference, _decode_time_difference),
    (Timestamp, _decode_time_timestamp),
    (U8, lambda x: _decode_uint(x, 1)),
    (U16, lambda x: _decode_uint(x, 2)),
    (U32, lambda x: _decode_uint(x, 4)),
    (U64, lambda x: _decode_uint(x, 8)),
    (U128, _decode_uint_big),
    (U256, _decode_uint_big),
    (U512, _decode_uint_big),
})
