import typing

from pycspr.serialisation import byte_array as byte_array_codec
# from pycspr.serialisation import dictionary as dictionary_codec
from pycspr.serialisation import json as json_codec



# Map: encoding <-> serialisation.
_CODECS = {
    "bytes": byte_array_codec,
    # "dict": dictionary_codec,
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

# Entity to dictionary mapper.
# to_dict = lambda e: _encode(e, "dict")

# Entity to JSON mapper.
to_json = lambda e: _encode(e, "json")

# Dictionary to entity.
# from_dict = lambda obj: json_codec.decode(obj)

# JSON to entity.
from_json = lambda obj: json_codec.decode(obj)
