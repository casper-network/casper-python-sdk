from pycspr.codec.byte_array import cl_bytearray


# Encodes parsed data.
encode = lambda v: cl_bytearray.encode(v.encode("utf-8"))

