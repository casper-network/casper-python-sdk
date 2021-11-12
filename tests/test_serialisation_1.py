from pycspr import serialisation
from pycspr.types import CLType
from pycspr.types import CLValue


def test_that_cl_types_serialise_to_bytes(cl_types_vector):
    for cl_type in cl_types_vector:
        assert cl_type == serialisation.from_bytes(serialisation.to_bytes(cl_type))


def test_that_cl_types_serialise_to_json(cl_types_vector):
    for cl_type in cl_types_vector:
        assert cl_type == serialisation.from_json(CLType, serialisation.to_json(cl_type))


def test_that_cl_values_serialise_to_bytes(cl_values_vector):
    for cl_value in cl_values_vector:
        assert cl_value == serialisation.from_bytes(serialisation.to_bytes(cl_value))


def test_that_cl_values_serialise_to_json(cl_values_vector):
    for cl_value in cl_values_vector:
        assert cl_value == serialisation.from_json(CLValue, serialisation.to_json(cl_value))
