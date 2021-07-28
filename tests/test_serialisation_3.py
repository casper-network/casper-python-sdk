import pycspr


def test_cl_types_simple(vector_cl_types):
    for type_key in pycspr.types.TYPES_SIMPLE:
        vector = vector_cl_types.get_vector(type_key)
        if not vector["hex"]:
            continue
        
        if type_key.name == "UREF":
            vector["value"] = pycspr.factory.create_uref_from_string(vector["value"])

        cl_type = pycspr.factory.create_cl_type_of_simple(type_key)
        cl_value = pycspr.factory.create_cl_value(cl_type, vector["value"])
        assert pycspr.serialisation.to_bytes(cl_value).hex() == vector["hex"]

    raise NotImplementedError("TODO: finish implmenting test around cl values")
