from pycspr.serialisation import byte_array as byte_array_codec
from pycspr.serialisation import dictionary as dictionary_codec
from pycspr.serialisation import json as json_codec



# Maps an entity to a byte array.
to_bytes = byte_array_codec.encode

# Maps an entity to a dictionary.
to_dict = dictionary_codec.encode

# Maps an entity to JSON.
to_json = json_codec.encode

# Maps a byte array to a domain entity.
from_bytes = byte_array_codec.decode

# Maps a dictionary to a domain entity.
from_dict = dictionary_codec.decode

# Maps JSON to a domain entity.
from_json = json_codec.decode
