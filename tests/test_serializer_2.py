from pycspr import serializer


def test_that_cl_values_serialisation_to_and_from_bytes(cl_values_vector):
    for entity in cl_values_vector:
        encoded = serializer.to_bytes(entity)
        assert isinstance(encoded, bytes)
        cl_typedef = serializer.clv_to_clt(entity)
        _, decoded = serializer.from_bytes(cl_typedef, encoded)
        assert entity == decoded


def test_that_cl_values_serialisation_to_and_from_json(cl_values_vector):
    for entity in cl_values_vector:
        encoded = serializer.to_json(entity)
        assert isinstance(encoded, dict)
        decoded = serializer.from_json(type(entity), encoded)
        assert entity == decoded
