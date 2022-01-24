from pycspr import serialisation


def test_that_cl_types_serialisation_to_and_from_bytes(cl_types_vector):
    for entity in cl_types_vector:
        encoded = serialisation.to_bytes(entity)
        assert isinstance(encoded, bytes)
        _, decoded = serialisation.from_bytes(encoded)
        assert entity == decoded


def test_that_cl_types_serialisation_to_and_from_json(cl_types_vector):
    for entity in cl_types_vector:
        encoded = serialisation.to_json(entity)
        assert isinstance(encoded, (str, dict))
        assert entity == serialisation.from_json(encoded)
