from pycspr.serialisation import byte_array as _byte_array
from pycspr.serialisation import json as _json


# Maps a domain entity to a byte array.
to_bytes = _byte_array.encode

# Maps a domain entity to JSON.
to_json = _json.encode

# Maps a byte array to a domain entity.
from_bytes = _byte_array.decode

# Maps JSON to a domain entity.
from_json = _json.decode
