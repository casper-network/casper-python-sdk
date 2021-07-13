import typing

from pycspr.codec import byte_array as byte_array_codec
from pycspr.codec import hex_string as hex_string_codec
from pycspr.codec import json as json_codec



# Map: encoding <-> codec.
_CODECS = {
    "bytes": byte_array_codec,
    "hex": hex_string_codec,
    "json": json_codec,
}


def _encode(entity: object, encoding: str = "json") -> typing.Union[typing.List[int], str]:
    """Maps a domain entity to a supported representation.
    
    """
    if encoding not in _CODECS:
        raise ValueError(f"Invalid encoding: {encoding}.  Must be one of: {_CODECS.keys()}")

    return _CODECS[encoding].encode(entity)


# Entity to byte array mapper.
to_bytes = lambda e: _encode(e, "bytes")

# Entity to hex string mapper.
to_hex = lambda e: _encode(e, "hex")

# Entity to JSON mapper.
to_json = lambda e: _encode(e, "json")

# JSON to entity.
from_json = lambda obj: json_codec.decode(obj)
