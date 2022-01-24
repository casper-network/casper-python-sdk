from pycspr import serialisation


def test_that_cl_values_serialisation_to_and_from_bytes(cl_values_vector):
    for entity in cl_values_vector:
        encoded = serialisation.to_bytes(entity)
        assert isinstance(encoded, bytes)
        cl_type = serialisation.cl_value_to_cl_type(entity)
        _, decoded = serialisation.from_bytes(encoded, cl_type)
        assert entity == decoded


def test_that_cl_values_serialisation_to_and_from_json(cl_values_vector):
    for entity in cl_values_vector:
        encoded = serialisation.to_json(entity)
        assert isinstance(encoded, dict)
        decoded = serialisation.from_json(encoded, type(entity))
        assert entity == decoded
