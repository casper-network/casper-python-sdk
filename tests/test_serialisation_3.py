import pycspr
from pycspr.types import CLTypeKey


def test_that_cl_simple_types_can_be_encoded_to_bytes(vector_cl_types):
    def yield_vectors():
        for type_key in vector_cl_types.SIMPLE_TYPES:
            for vector in vector_cl_types.get_vectors(type_key):
                yield vector, type_key

    for vector, type_key in yield_vectors():
        cl_type = None
        if type_key == CLTypeKey.BOOL:
            cl_type = pycspr.cl_type_factory.boolean()
        elif type_key == CLTypeKey.BYTE_ARRAY:
            cl_type = pycspr.cl_type_factory.byte_array(32)

        if cl_type:
            cl_value = pycspr.cl_value.create(cl_type, vector["value"])
            assert pycspr.to_bytes(cl_value).hex() == vector["hex"], vector["typeof"]
