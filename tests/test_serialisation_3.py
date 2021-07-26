def test_cl_types_simple(LIB, FACTORY, TYPES, vector_cl_data_1):
    for type_key in TYPES.TYPES_SIMPLE:
        if type_key.name == "UREF":
            vector = vector_cl_data_1.get_vector(type_key)
            cl_type = FACTORY.create_cl_type_of_simple(type_key)
            cl_value = FACTORY.create_cl_value(cl_type, vector["value"])

            print(vector)
            print(cl_value)

            print(LIB.serialisation.to_bytes(cl_value).hex())


    raise NotImplementedError()