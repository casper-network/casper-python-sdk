import typing

from pycspr.api.node.bin.codec.encoder.request_core import \
    ENCODERS as _ENCODERS_1
from pycspr.api.node.bin.codec.encoder.request_get_information import \
    ENCODERS as _ENCODERS_2
from pycspr.api.node.bin.codec.encoder.request_get_record import \
    ENCODERS as _ENCODERS_3
from pycspr.api.node.bin.codec.encoder.request_get_state import \
    ENCODERS as _ENCODERS_4

ENCODERS: typing.Dict[typing.Type, typing.Callable] = \
    _ENCODERS_1 | _ENCODERS_2 | _ENCODERS_3 | _ENCODERS_4
