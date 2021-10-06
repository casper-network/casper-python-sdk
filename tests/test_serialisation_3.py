from pycspr import factory
from pycspr import types
from pycspr import serialisation


def test_that_cl_simple_types_can_be_encoded_to_bytes(vector_cl_types):
    def yield_vectors():
        for type_key in types.TYPES_SIMPLE:
            for vector in vector_cl_types.get_vectors(type_key):
                yield vector, type_key

    for vector, type_key in yield_vectors():
        cl_type = factory.create_cl_type_of_simple(type_key)
        cl_value = factory.create_cl_value(cl_type, vector["value"])
        assert serialisation.to_bytes(cl_value).hex() == vector["hex"], vector["typeof"]
