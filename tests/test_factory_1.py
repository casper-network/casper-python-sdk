def test_create_execution_arg_simple(CL_FACTORY, CL_TYPES, DEPLOY_FACTORY, DEPLOY_TYPES, vector_cl_data_1):
    for type_key in CL_TYPES.CL_TYPES_SIMPLE:
        vector = vector_cl_data_1.get_vector(type_key)
        cl_type = CL_FACTORY.create_simple(type_key)
        _assert_arg(CL_FACTORY, DEPLOY_FACTORY, DEPLOY_TYPES, vector["value"], cl_type)


def test_create_execution_arg_byte_array(CL_FACTORY, CL_TYPES, DEPLOY_FACTORY, DEPLOY_TYPES, vector_cl_data_1):
    type_key = CL_TYPES.CLTypeKey.BYTE_ARRAY
    vector = vector_cl_data_1.get_vector(type_key)
    value = bytes.fromhex(vector["value"])
    size = len(value)
    cl_type = CL_FACTORY.create_byte_array(size)
    _assert_arg(CL_FACTORY, DEPLOY_FACTORY, DEPLOY_TYPES, value, cl_type)


def test_create_execution_arg_list(CL_FACTORY, CL_TYPES, DEPLOY_FACTORY, DEPLOY_TYPES, vector_cl_data_1):
    type_key = CL_TYPES.CLTypeKey.LIST
    vector = vector_cl_data_1.get_vector(type_key)
    type_key_item = CL_TYPES.CLTypeKey[vector["typeof_item"]]
    if type_key_item in CL_TYPES.CL_TYPES_SIMPLE:
        cl_type_item = CL_FACTORY.create_simple(type_key_item)
        cl_type = CL_FACTORY.create_list(cl_type_item)
        _assert_arg(CL_FACTORY, DEPLOY_FACTORY, DEPLOY_TYPES, vector["value"], cl_type)


def test_create_execution_arg_map(CL_FACTORY, CL_TYPES, DEPLOY_FACTORY, DEPLOY_TYPES, vector_cl_data_1):
    type_key = CL_TYPES.CLTypeKey.MAP
    for vector in vector_cl_data_1.get_vectors(type_key):
        type_key_of_map_key = CL_TYPES.CLTypeKey[vector["typeof_key"]]
        type_key_of_map_value = CL_TYPES.CLTypeKey[vector["typeof_value"]]
        if type_key_of_map_key in CL_TYPES.CL_TYPES_SIMPLE and type_key_of_map_value in CL_TYPES.CL_TYPES_SIMPLE:
            cl_type_map_key = CL_FACTORY.create_simple(type_key_of_map_key)
            cl_type_map_value = CL_FACTORY.create_simple(type_key_of_map_value)
            cl_type = CL_FACTORY.create_map(cl_type_map_key, cl_type_map_value)
            _assert_arg(CL_FACTORY, DEPLOY_FACTORY, DEPLOY_TYPES, vector["value"], cl_type)


def test_create_execution_arg_tuple_1(CL_FACTORY, CL_TYPES, DEPLOY_FACTORY, DEPLOY_TYPES, vector_cl_data_1):
    type_key = CL_TYPES.CLTypeKey.TUPLE_1
    for vector in vector_cl_data_1.get_vectors(type_key):
        type_key_t0 = CL_TYPES.CLTypeKey[vector["typeof_t0"]]
        if type_key_t0 in CL_TYPES.CL_TYPES_SIMPLE:
            cl_type_t0 = CL_FACTORY.create_simple(type_key_t0)
            cl_type = CL_FACTORY.create_tuple_1(cl_type_t0)
            _assert_arg(CL_FACTORY, DEPLOY_FACTORY, DEPLOY_TYPES, vector["value"], cl_type)


def test_create_execution_arg_tuple_2(CL_FACTORY, CL_TYPES, DEPLOY_FACTORY, DEPLOY_TYPES, vector_cl_data_1):
    type_key = CL_TYPES.CLTypeKey.TUPLE_2
    for vector in vector_cl_data_1.get_vectors(type_key):
        type_key_t0 = CL_TYPES.CLTypeKey[vector["typeof_t0"]]
        type_key_t1 = CL_TYPES.CLTypeKey[vector["typeof_t1"]]
        if type_key_t0 in CL_TYPES.CL_TYPES_SIMPLE and type_key_t1 in CL_TYPES.CL_TYPES_SIMPLE:
            cl_type_t0 = CL_FACTORY.create_simple(type_key_t0)
            cl_type_t1 = CL_FACTORY.create_simple(type_key_t1)
            cl_type = CL_FACTORY.create_tuple_2(cl_type_t0, cl_type_t1)
            _assert_arg(CL_FACTORY, DEPLOY_FACTORY, DEPLOY_TYPES, vector["value"], cl_type)


def test_create_execution_arg_tuple_3(CL_FACTORY, CL_TYPES, DEPLOY_FACTORY, DEPLOY_TYPES, vector_cl_data_1):
    type_key = CL_TYPES.CLTypeKey.TUPLE_3
    for vector in vector_cl_data_1.get_vectors(type_key):
        type_key_t0 = CL_TYPES.CLTypeKey[vector["typeof_t0"]]
        type_key_t1 = CL_TYPES.CLTypeKey[vector["typeof_t1"]]
        type_key_t2 = CL_TYPES.CLTypeKey[vector["typeof_t2"]]
        if type_key_t0 in CL_TYPES.CL_TYPES_SIMPLE and type_key_t1 in \
            CL_TYPES.CL_TYPES_SIMPLE and type_key_t2 in CL_TYPES.CL_TYPES_SIMPLE:
            cl_type_t0 = CL_FACTORY.create_simple(type_key_t0)
            cl_type_t1 = CL_FACTORY.create_simple(type_key_t1)
            cl_type_t2 = CL_FACTORY.create_simple(type_key_t2)
            cl_type = CL_FACTORY.create_tuple_3(cl_type_t0, cl_type_t1, cl_type_t2)
            _assert_arg(CL_FACTORY, DEPLOY_FACTORY, DEPLOY_TYPES, vector["value"], cl_type)


def _assert_arg(CL_FACTORY, DEPLOY_FACTORY, DEPLOY_TYPES, value, cl_type):
    # Assert arg can be instantiated.
    arg_name = f"a-{cl_type.typeof.name.lower()}-arg"
    arg = DEPLOY_FACTORY.create_execution_arg(arg_name, cl_type, value)
    assert isinstance(arg, DEPLOY_TYPES.ExecutionArgument)

    # Assert optional arg can be instantiated.
    cl_type = CL_FACTORY.create_option(cl_type)
    for value in [value, None]:
        arg = DEPLOY_FACTORY.create_execution_arg(f"{arg_name}-optional", cl_type, value)
        assert isinstance(arg, DEPLOY_TYPES.ExecutionArgument)
