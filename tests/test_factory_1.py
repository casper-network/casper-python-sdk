def test_create_named_arg_simple(FACTORY, TYPES, vectors_1):
    for cl_type in TYPES.CL_TYPES_SIMPLE:
        vector = vectors_1.get_vector(cl_type)
        cl_type_info = FACTORY.cl_type.create_simple(cl_type)
        _assert_arg(FACTORY, TYPES, vector["value"], cl_type_info)


def test_create_named_arg_byte_array(FACTORY, TYPES, vectors_1):
    cl_type = TYPES.CLType.BYTE_ARRAY
    vector = vectors_1.get_vector(cl_type)
    value = bytes.fromhex(vector["value"])
    size = len(value)
    cl_type_info = FACTORY.cl_type.create_byte_array(size)
    _assert_arg(FACTORY, TYPES, value, cl_type_info)


def test_create_named_arg_list(FACTORY, TYPES, vectors_1):
    cl_type = TYPES.CLType.LIST
    vector = vectors_1.get_vector(cl_type)
    cl_type_item = TYPES.CLType[vector["typeof_item"]]

    if cl_type_item in TYPES.CL_TYPES_SIMPLE:
        cl_type_info_item = FACTORY.cl_type.create_simple(cl_type_item)
        cl_type_info = FACTORY.cl_type.create_list(cl_type_info_item)
        _assert_arg(FACTORY, TYPES, vector["value"], cl_type_info)


def test_create_named_arg_map(FACTORY, TYPES, vectors_1):
    cl_type = TYPES.CLType.MAP
    for vector in vectors_1.get_vectors(cl_type):
        cl_type_key = TYPES.CLType[vector["typeof_key"]]
        cl_type_value = TYPES.CLType[vector["typeof_value"]]
        if cl_type_key in TYPES.CL_TYPES_SIMPLE and cl_type_value in TYPES.CL_TYPES_SIMPLE:
            cl_type_info_key = FACTORY.cl_type.create_simple(cl_type_key)
            cl_type_info_value = FACTORY.cl_type.create_simple(cl_type_value)
            cl_type_info = FACTORY.cl_type.create_map(cl_type_info_key, cl_type_info_value)
            _assert_arg(FACTORY, TYPES, vector["value"], cl_type_info)


def test_create_named_arg_tuple_1(FACTORY, TYPES, vectors_1):
    cl_type = TYPES.CLType.TUPLE_1
    for vector in vectors_1.get_vectors(cl_type):
        cl_type_t0 = TYPES.CLType[vector["typeof_t0"]]
        if cl_type_t0 in TYPES.CL_TYPES_SIMPLE:
            cl_type_info_t0 = FACTORY.cl_type.create_simple(cl_type_t0)
            cl_type_info = FACTORY.cl_type.create_tuple_1(cl_type_info_t0)
            _assert_arg(FACTORY, TYPES, vector["value"], cl_type_info)


def test_create_named_arg_tuple_2(FACTORY, TYPES, vectors_1):
    cl_type = TYPES.CLType.TUPLE_2
    for vector in vectors_1.get_vectors(cl_type):
        cl_type_t0 = TYPES.CLType[vector["typeof_t0"]]
        cl_type_t1 = TYPES.CLType[vector["typeof_t1"]]
        if cl_type_t0 in TYPES.CL_TYPES_SIMPLE and cl_type_t1 in TYPES.CL_TYPES_SIMPLE:
            cl_type_info_t0 = FACTORY.cl_type.create_simple(cl_type_t0)
            cl_type_info_t1 = FACTORY.cl_type.create_simple(cl_type_t1)
            cl_type_info = FACTORY.cl_type.create_tuple_2(cl_type_info_t0, cl_type_info_t1)
            _assert_arg(FACTORY, TYPES, vector["value"], cl_type_info)


def test_create_named_arg_tuple_3(FACTORY, TYPES, vectors_1):
    cl_type = TYPES.CLType.TUPLE_3
    for vector in vectors_1.get_vectors(cl_type):
        cl_type_t0 = TYPES.CLType[vector["typeof_t0"]]
        cl_type_t1 = TYPES.CLType[vector["typeof_t1"]]
        cl_type_t2 = TYPES.CLType[vector["typeof_t2"]]
        if cl_type_t0 in TYPES.CL_TYPES_SIMPLE and cl_type_t1 in TYPES.CL_TYPES_SIMPLE and cl_type_t2 in TYPES.CL_TYPES_SIMPLE:
            cl_type_info_t0 = FACTORY.cl_type.create_simple(cl_type_t0)
            cl_type_info_t1 = FACTORY.cl_type.create_simple(cl_type_t1)
            cl_type_info_t2 = FACTORY.cl_type.create_simple(cl_type_t2)
            cl_type_info = FACTORY.cl_type.create_tuple_3(cl_type_info_t0, cl_type_info_t1, cl_type_info_t2)
            _assert_arg(FACTORY, TYPES, vector["value"], cl_type_info)


def _assert_arg(FACTORY, TYPES, value, cl_type):
    # Assert named arg can be instantiated.
    arg_name = f"a-{cl_type.typeof.name.lower()}-arg"
    arg = FACTORY.deploys.create_named_arg(arg_name, cl_type, value)
    assert isinstance(arg, TYPES.DeployNamedArg)

    # Assert optional named arg can be instantiated.
    cl_type = FACTORY.cl_type.create_option(cl_type)
    for value in [value, None]:
        arg = FACTORY.deploys.create_named_arg(f"{arg_name}-optional", cl_type, value)
        assert isinstance(arg, TYPES.DeployNamedArg)
