import pycspr


def test_that_cl_simple_types_can_be_encoded_to_bytes(vector_cl_types):
    for type_key in pycspr.types.TYPES_SIMPLE:
        vector = vector_cl_types.get_vector(type_key)
        cl_type = pycspr.factory.create_cl_type_of_simple(type_key)
        cl_value = pycspr.factory.create_cl_value(cl_type, vector["value"])
        assert pycspr.serialisation.to_bytes(cl_value).hex() == vector["hex"], vector["typeof"]

