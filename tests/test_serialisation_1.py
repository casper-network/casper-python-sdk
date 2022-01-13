from pycspr import serialisation


def test_that_cl_types_serialisation_to_and_from_bytes(cl_types_vector):
    for cl_type in cl_types_vector:
        as_bytes = serialisation.cl_type_to_bytes(cl_type)
        assert isinstance(as_bytes, bytes)
        _, from_bytes = serialisation.cl_type_from_bytes(as_bytes)
        assert cl_type == from_bytes


def test_that_cl_types_serialisation_to_and_from_json(cl_types_vector):
    for cl_type in cl_types_vector:
        as_json = serialisation.cl_type_to_json(cl_type)
        assert isinstance(as_json, (str, dict))
        assert cl_type == serialisation.cl_type_from_json(as_json)
