import pycspr


def test_that_cl_simple_types_can_be_encoded_to_bytes(vector_cl_types):
    def yield_vectors():
        for type_key in pycspr.types.TYPES_SIMPLE:
            for vector in vector_cl_types.get_vectors(type_key):
                yield vector, type_key

    for vector, type_key in yield_vectors():
        cl_type = pycspr.cl_type_factory.simple(type_key)
        print(cl_type)
        cl_value = pycspr.cl_value.create(vector["value"], cl_type)
        assert pycspr.serialisation.to_bytes(cl_value).hex() == vector["hex"], vector["typeof"]
