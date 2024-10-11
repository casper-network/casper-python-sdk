import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.numeric import U64, TimeDifference, Timestamp


def _decode_time_difference(bytes_in: bytes) -> typing.Tuple[bytes, TimeDifference]:
    assert len(bytes_in) >= 4
    rem, timediff_ms = decode(U64, bytes_in)
    return rem, Timestamp(timediff_ms)


def _decode_time_timestamp(bytes_in: bytes) -> typing.Tuple[bytes, Timestamp]:
    assert len(bytes_in) >= 4
    rem, ts_ms = decode(U64, bytes_in)
    return rem, Timestamp(float(ts_ms))


register_decoders({
    (TimeDifference, _decode_time_difference),
    (Timestamp, _decode_time_timestamp),
})
