from pycspr import serialisation


def test_serialisation_of_cl_types_to_bytes(cl_types_vector):
    for cl_type in cl_types_vector:
        as_bytes = serialisation.cl_type_to_bytes(cl_type)
        assert isinstance(as_bytes, bytes)
        _, from_bytes = serialisation.cl_type_from_bytes(as_bytes)
        assert cl_type == from_bytes
    # raise ValueError()


def test_serialisation_of_cl_types_to_json(cl_types_vector):
    for cl_type in cl_types_vector:
        as_json = serialisation.cl_type_to_json(cl_type)
        assert isinstance(as_json, (str, dict))
        assert cl_type == serialisation.cl_type_from_json(as_json)


def test_serialisation_of_cl_values_to_bytes(cl_values_vector):
    for cl_value in cl_values_vector:
        as_bytes = serialisation.cl_value_to_bytes(cl_value)
        assert isinstance(as_bytes, bytes)
        cl_type = serialisation.cl_value_to_cl_type(cl_value)
        _, cl_value_1 = serialisation.cl_value_from_bytes(as_bytes, cl_type)
        assert cl_value == cl_value_1


def test_serialisation_of_cl_values_to_json(cl_values_vector):
    for cl_value in cl_values_vector:
        as_json = serialisation.cl_value_to_json(cl_value)
        assert isinstance(as_json, dict)
        assert cl_value == serialisation.cl_value_from_json(as_json)
