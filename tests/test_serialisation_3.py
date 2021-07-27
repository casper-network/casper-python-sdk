def test_cl_types_simple(LIB, FACTORY, TYPES, vector_cl_data_1):
    for type_key in TYPES.TYPES_SIMPLE:
        vector = vector_cl_data_1.get_vector(type_key)
        if not vector["hex"]:
            continue
        
        if type_key.name == "UREF":
            vector["value"] = FACTORY.create_uref_from_string(vector["value"])

        cl_type = FACTORY.create_cl_type_of_simple(type_key)
        cl_value = FACTORY.create_cl_value(cl_type, vector["value"])
        assert LIB.serialisation.to_bytes(cl_value).hex() == vector["hex"]

    raise NotImplementedError("TODO: finish implmenting test around cl values")