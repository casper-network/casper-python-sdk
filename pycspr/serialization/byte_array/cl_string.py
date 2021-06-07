from pycspr.serialization.utils import CLType



# Formal type within CL type system.
TYPEOF = CLType.STRING

# Default character encoding.
_ENCODING = "utf-8"


# Decodes input data.
decode = lambda v: bytes(v).decode(_ENCODING)


# Encodes a domain type instance.
encode = lambda v: [i for i in v.encode(_ENCODING)]


# Returns length in bytes of encoded data.
get_encoded_length = lambda v: len(bytes(data))


# A predicate returning a flag indicating whether encoded data can be decoded.
is_decodeable = lambda encoded: isinstance(encoded, list)


# A predicate returning a flag indicating whether domain type instance can be encoded.
is_encodeable = lambda value: isinstance(value, str)
