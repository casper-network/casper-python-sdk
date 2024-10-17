from pycspr import serializer
from pycspr.type_defs.cl_types import CLT_Type


def test_that_cl_types_serialisation_to_and_from_bytes(cl_types_vector):
    for entity in cl_types_vector:
        encoded = serializer.to_bytes(entity)
        assert isinstance(encoded, bytes)
        _, decoded = serializer.from_bytes(CLT_Type, encoded)
        assert entity == decoded


def test_that_cl_types_serialisation_to_and_from_json(cl_types_vector):
    for entity in cl_types_vector:
        encoded = serializer.to_json(entity)
        assert isinstance(encoded, (str, dict))
        decoded = serializer.from_json(type(entity), encoded)
        assert entity == decoded
