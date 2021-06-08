def test_create_execution_arg_simple(FACTORY, TYPES, vectors_1):
    for type_key in TYPES.CL_TYPES_SIMPLE:
        vector = vectors_1.get_vector(type_key)
        cl_type = FACTORY.cl_types.create_simple(type_key)
        _assert_arg(FACTORY, TYPES, vector["value"], cl_type)


def test_create_execution_arg_byte_array(FACTORY, TYPES, vectors_1):
    type_key = TYPES.CLTypeKey.BYTE_ARRAY
    vector = vectors_1.get_vector(type_key)
    value = bytes.fromhex(vector["value"])
    size = len(value)
    cl_type = FACTORY.cl_types.create_byte_array(size)
    _assert_arg(FACTORY, TYPES, value, cl_type)


def test_create_execution_arg_list(FACTORY, TYPES, vectors_1):
    type_key = TYPES.CLTypeKey.LIST
    vector = vectors_1.get_vector(type_key)
    type_key_item = TYPES.CLTypeKey[vector["typeof_item"]]
    if type_key_item in TYPES.CL_TYPES_SIMPLE:
        cl_type_item = FACTORY.cl_types.create_simple(type_key_item)
        cl_type = FACTORY.cl_types.create_list(cl_type_item)
        _assert_arg(FACTORY, TYPES, vector["value"], cl_type)


def test_create_execution_arg_map(FACTORY, TYPES, vectors_1):
    type_key = TYPES.CLTypeKey.MAP
    for vector in vectors_1.get_vectors(type_key):
        type_key_of_map_key = TYPES.CLTypeKey[vector["typeof_key"]]
        type_key_of_map_value = TYPES.CLTypeKey[vector["typeof_value"]]
        if type_key_of_map_key in TYPES.CL_TYPES_SIMPLE and type_key_of_map_value in TYPES.CL_TYPES_SIMPLE:
            cl_type_map_key = FACTORY.cl_types.create_simple(type_key_of_map_key)
            cl_type_map_value = FACTORY.cl_types.create_simple(type_key_of_map_value)
            cl_type = FACTORY.cl_types.create_map(cl_type_map_key, cl_type_map_value)
            _assert_arg(FACTORY, TYPES, vector["value"], cl_type)


def test_create_execution_arg_tuple_1(FACTORY, TYPES, vectors_1):
    type_key = TYPES.CLTypeKey.TUPLE_1
    for vector in vectors_1.get_vectors(type_key):
        type_key_t0 = TYPES.CLTypeKey[vector["typeof_t0"]]
        if type_key_t0 in TYPES.CL_TYPES_SIMPLE:
            cl_type_t0 = FACTORY.cl_types.create_simple(type_key_t0)
            cl_type = FACTORY.cl_types.create_tuple_1(cl_type_t0)
            _assert_arg(FACTORY, TYPES, vector["value"], cl_type)


def test_create_execution_arg_tuple_2(FACTORY, TYPES, vectors_1):
    type_key = TYPES.CLTypeKey.TUPLE_2
    for vector in vectors_1.get_vectors(type_key):
        type_key_t0 = TYPES.CLTypeKey[vector["typeof_t0"]]
        type_key_t1 = TYPES.CLTypeKey[vector["typeof_t1"]]
        if type_key_t0 in TYPES.CL_TYPES_SIMPLE and type_key_t1 in TYPES.CL_TYPES_SIMPLE:
            cl_type_t0 = FACTORY.cl_types.create_simple(type_key_t0)
            cl_type_t1 = FACTORY.cl_types.create_simple(type_key_t1)
            cl_type = FACTORY.cl_types.create_tuple_2(cl_type_t0, cl_type_t1)
            _assert_arg(FACTORY, TYPES, vector["value"], cl_type)


def test_create_execution_arg_tuple_3(FACTORY, TYPES, vectors_1):
    type_key = TYPES.CLTypeKey.TUPLE_3
    for vector in vectors_1.get_vectors(type_key):
        type_key_t0 = TYPES.CLTypeKey[vector["typeof_t0"]]
        type_key_t1 = TYPES.CLTypeKey[vector["typeof_t1"]]
        type_key_t2 = TYPES.CLTypeKey[vector["typeof_t2"]]
        if type_key_t0 in TYPES.CL_TYPES_SIMPLE and type_key_t1 in TYPES.CL_TYPES_SIMPLE and type_key_t2 in TYPES.CL_TYPES_SIMPLE:
            cl_type_t0 = FACTORY.cl_types.create_simple(type_key_t0)
            cl_type_t1 = FACTORY.cl_types.create_simple(type_key_t1)
            cl_type_t2 = FACTORY.cl_types.create_simple(type_key_t2)
            cl_type = FACTORY.cl_types.create_tuple_3(cl_type_t0, cl_type_t1, cl_type_t2)
            _assert_arg(FACTORY, TYPES, vector["value"], cl_type)


def _assert_arg(FACTORY, TYPES, value, cl_type):
    # Assert arg can be instantiated.
    arg_name = f"a-{cl_type.typeof.name.lower()}-arg"
    arg = FACTORY.deploys.create_execution_arg(arg_name, cl_type, value)
    assert isinstance(arg, TYPES.ExecutionArgument)

    # Assert optional arg can be instantiated.
    cl_type = FACTORY.cl_types.create_option(cl_type)
    for value in [value, None]:
        arg = FACTORY.deploys.create_execution_arg(f"{arg_name}-optional", cl_type, value)
        assert isinstance(arg, TYPES.ExecutionArgument)
