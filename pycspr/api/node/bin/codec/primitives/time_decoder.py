import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.primitives.numeric import U64
from pycspr.api.node.bin.types.primitives.time import TimeDifference, Timestamp


def _decode_time_difference(bytes_in: bytes) -> typing.Tuple[bytes, TimeDifference]:
    assert len(bytes_in) >= 4
    bytes_rem, timediff_ms = decode(U64, bytes_in)
    return bytes_rem, Timestamp(timediff_ms)


def _decode_time_timestamp(bytes_in: bytes) -> typing.Tuple[bytes, Timestamp]:
    assert len(bytes_in) >= 4
    bytes_rem, ts_ms = decode(U64, bytes_in)
    return bytes_rem, Timestamp(float(ts_ms))


register_decoders({
    (TimeDifference, _decode_time_difference),
    (Timestamp, _decode_time_timestamp),
})
