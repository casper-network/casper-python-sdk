from pycspr.serialisation import bytearray as _bytearray


# Mapper: domain entity -> byte array.
to_bytes = _bytearray.to_bytes

# Mapper: domain entity -> JSON text blob.
to_json = _bytearray.to_json

# Mapper: byte array -> domain entity.
from_bytes = _bytearray.from_bytes

# Mapper: JSON text blob -> domain entity.
from_json = _bytearray.from_json
