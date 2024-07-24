import typing

from pycspr.api.node.bin.codec.encoder.requests.core import \
    ENCODERS as _ENCODERS_CORE
from pycspr.api.node.bin.codec.encoder.requests.get import \
    ENCODERS as _ENCODERS_GET


ENCODERS: typing.Dict[typing.Type, typing.Callable] = _ENCODERS_CORE | _ENCODERS_GET
