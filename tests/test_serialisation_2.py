from pycspr import serialisation


def test_that_cl_values_serialisation_to_and_from_bytes(cl_values_vector):
    for cl_value in cl_values_vector:
        as_bytes = serialisation.cl_value_to_bytes(cl_value)
        assert isinstance(as_bytes, bytes)
        cl_type = serialisation.cl_value_to_cl_type(cl_value)
        _, cl_value_1 = serialisation.cl_value_from_bytes(as_bytes, cl_type)
        assert cl_value == cl_value_1


def test_that_cl_values_serialisation_to_and_from_json(cl_values_vector):
    for cl_value in cl_values_vector:
        as_json = serialisation.cl_value_to_json(cl_value)
        assert isinstance(as_json, dict)
        assert cl_value == serialisation.cl_value_from_json(as_json)
