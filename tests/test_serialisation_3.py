import pycspr


def test_cl_types_simple(vector_cl_types):
    for type_key in pycspr.types.TYPES_SIMPLE:
        if type_key.name == "UREF":
            continue

        vector = vector_cl_types.get_vector(type_key)

        
        #     vector["value"] = pycspr.factory.create_uref_from_string(vector["value"])

        cl_type = pycspr.factory.create_cl_type_of_simple(type_key)
        cl_value = pycspr.factory.create_cl_value(cl_type, vector["value"])
        print(type_key, pycspr.serialisation.to_bytes(cl_value).hex())
        # assert pycspr.serialisation.to_bytes(cl_value).hex() == vector["hex"]

    raise NotImplementedError("TODO: finish implmenting test around cl values")
