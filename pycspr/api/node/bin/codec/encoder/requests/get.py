import typing

from pycspr.api.node.bin.codec.encoder.requests.get_information import \
    ENCODERS as _ENCODERS_1
from pycspr.api.node.bin.codec.encoder.requests.get_record import \
    ENCODERS as _ENCODERS_2
from pycspr.api.node.bin.codec.encoder.requests.get_state import \
    ENCODERS as _ENCODERS_3

ENCODERS: typing.Dict[typing.Type, typing.Callable] = _ENCODERS_1 | _ENCODERS_2 | _ENCODERS_3
