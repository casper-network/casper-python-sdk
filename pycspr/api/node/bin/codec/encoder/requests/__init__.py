import typing

from pycspr.api.node.bin.codec.encoder.requests.core import \
    ENCODERS as _ENCODERS_1
from pycspr.api.node.bin.codec.encoder.requests.get import \
    ENCODERS as _ENCODERS_2


ENCODERS: typing.Dict[typing.Type, typing.Callable] = _ENCODERS_1 | _ENCODERS_2
