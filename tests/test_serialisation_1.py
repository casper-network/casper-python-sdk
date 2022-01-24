from pycspr import serialisation1


def test_that_cl_types_serialisation_to_and_from_bytes(cl_types_vector):
    for entity in cl_types_vector:
        encoded = serialisation1.to_bytes(entity)
        assert isinstance(encoded, bytes)
        _, decoded = serialisation1.from_bytes(encoded)
        assert entity == decoded


def test_that_cl_types_serialisation_to_and_from_json(cl_types_vector):
    for entity in cl_types_vector:
        encoded = serialisation1.to_json(entity)
        assert isinstance(encoded, (str, dict))
        assert entity == serialisation1.from_json(encoded)
