import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.primitives.numeric import U64
from pycspr.api.node.bin.types.primitives.time import Timestamp


def _decode_time_timestamp(bytes_in: bytes) -> typing.Tuple[bytes, Timestamp]:
    assert len(bytes_in) >= 4
    bytes_out, ts_ms = decode(U64, bytes_in)
    return bytes_out, Timestamp(float(ts_ms))


register_decoders({
    (Timestamp, _decode_time_timestamp),
})
