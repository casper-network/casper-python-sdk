import typing

from pycspr.api.node.bin.codec.encoder.requests.core import encode_request
from pycspr.api.node.bin.types.requests import Request


from pycspr.api.node.bin.codec.encoder.requests.get_information import \
    ENCODERS as _ENCODERS_GET_INFORMATION


ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    Request: encode_request
} | _ENCODERS_GET_INFORMATION
