import typing

from pycspr.api.node.bin.codec.decoder.responses.core import \
    DECODERS as _DECODERS_1

# Set of decoders within current scope.
DECODERS: typing.Dict[typing.Type, typing.Callable] = _DECODERS_1
