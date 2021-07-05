import typing

from pycspr.codec import byte_array as byte_array_encoder
from pycspr.codec import hex_string as hex_string_encoder
from pycspr.codec import json as json_encoder



# Map: encoding <-> codec.
_ENCODERS = {
    "byte-array": byte_array_encoder,
    "hex-string": hex_string_encoder,
    "json": json_encoder,
}


def encode(entity: object, encoding: str = "json") -> typing.Union[typing.List[int], str]:
    """Maps a domain entity to a supported representation.
    
    :param entity: Domain entity to be mapped.
    :param encoding: A supported domain entity encoding format.
    :returns: Appropriate representation of a domain entity.

    """
    if encoding not in _ENCODERS:
        raise ValueError(f"Invalid encoding: {encoding}")

    return _ENCODERS[encoding].encode(entity)
