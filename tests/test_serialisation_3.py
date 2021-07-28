import pycspr


def test_that_cl_simple_types_can_be_encoded_to_bytes(vector_cl_types):
    def yield_vectors():
        for type_key in pycspr.types.TYPES_SIMPLE:
            for vector in vector_cl_types.get_vectors(type_key):
                yield vector, type_key

    for vector, type_key in yield_vectors():
        cl_type = pycspr.factory.create_cl_type_of_simple(type_key)
        cl_value = pycspr.factory.create_cl_value(cl_type, vector["value"])
        assert pycspr.serialisation.to_bytes(cl_value).hex() == vector["hex"], vector["typeof"]
