import typing

from pycspr.api.node.bin.codec.decoder.domain import DECODERS as _DECODERS_1
from pycspr.api.node.bin.codec.decoder.request import DECODERS as _DECODERS_2
from pycspr.api.node.bin.codec.decoder.response import DECODERS as _DECODERS_3


DECODERS: typing.Dict[typing.Type, typing.Callable] = _DECODERS_1 | _DECODERS_2 | _DECODERS_3
