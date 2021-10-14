import pycspr



def test_create_deploy_arg_simple(vector_cl_types):
    for type_key in pycspr.types.TYPES_SIMPLE:
        for vector in vector_cl_types.get_vectors(type_key):
            cl_type = pycspr.cl_type_factory.simple(type_key)
            _assert_arg(vector["value"], cl_type)


def test_create_deploy_arg_byte_array(vector_cl_types):
    for vector in vector_cl_types.get_vectors(pycspr.types.CLTypeKey.BYTE_ARRAY):
        value = bytes.fromhex(vector["value"])
        cl_type = pycspr.cl_type_factory.byte_array(len(value))
        _assert_arg(value, cl_type)


def test_create_deploy_arg_list(vector_cl_types):
    for vector in vector_cl_types.get_vectors(pycspr.types.CLTypeKey.LIST):
        type_key_item = pycspr.types.CLTypeKey[vector["typeof_item"]]
        if type_key_item in pycspr.types.TYPES_SIMPLE:
            cl_type_item = pycspr.cl_type_factory.simple(type_key_item)
            cl_type = pycspr.cl_type_factory.list(cl_type_item)
            _assert_arg(vector["value"], cl_type)


def test_create_deploy_arg_map(vector_cl_types):
    for vector in vector_cl_types.get_vectors(pycspr.types.CLTypeKey.MAP):
        type_key_of_map_key = pycspr.types.CLTypeKey[vector["typeof_key"]]
        type_key_of_map_value = pycspr.types.CLTypeKey[vector["typeof_value"]]
        if type_key_of_map_key in pycspr.types.TYPES_SIMPLE and type_key_of_map_value in pycspr.types.TYPES_SIMPLE:
            cl_type_map_key = pycspr.cl_type_factory.simple(type_key_of_map_key)
            cl_type_map_value = pycspr.cl_type_factory.simple(type_key_of_map_value)
            cl_type = pycspr.cl_type_factory.map(cl_type_map_key, cl_type_map_value)
            _assert_arg(vector["value"], cl_type)


def test_create_deploy_arg_tuple_1(vector_cl_types):
    for vector in vector_cl_types.get_vectors(pycspr.types.CLTypeKey.TUPLE_1):
        type_key_t0 = pycspr.types.CLTypeKey[vector["typeof_t0"]]
        if type_key_t0 in pycspr.types.TYPES_SIMPLE:
            cl_type_t0 = pycspr.cl_type_factory.simple(type_key_t0)
            cl_type = pycspr.cl_type_factory.tuple_1(cl_type_t0)
            _assert_arg(vector["value"], cl_type)


def test_create_deploy_arg_tuple_2(vector_cl_types):
    for vector in vector_cl_types.get_vectors(pycspr.types.CLTypeKey.TUPLE_2):
        type_key_t0 = pycspr.types.CLTypeKey[vector["typeof_t0"]]
        type_key_t1 = pycspr.types.CLTypeKey[vector["typeof_t1"]]
        if type_key_t0 in pycspr.types.TYPES_SIMPLE and type_key_t1 in pycspr.types.TYPES_SIMPLE:
            cl_type_t0 = pycspr.cl_type_factory.simple(type_key_t0)
            cl_type_t1 = pycspr.cl_type_factory.simple(type_key_t1)
            cl_type = pycspr.cl_type_factory.tuple_2(cl_type_t0, cl_type_t1)
            _assert_arg(vector["value"], cl_type)


def test_create_deploy_arg_tuple_3(vector_cl_types):
    for vector in vector_cl_types.get_vectors(pycspr.types.CLTypeKey.TUPLE_3):
        type_key_t0 = pycspr.types.CLTypeKey[vector["typeof_t0"]]
        type_key_t1 = pycspr.types.CLTypeKey[vector["typeof_t1"]]
        type_key_t2 = pycspr.types.CLTypeKey[vector["typeof_t2"]]
        if type_key_t0 in pycspr.types.TYPES_SIMPLE and type_key_t1 in \
            pycspr.types.TYPES_SIMPLE and type_key_t2 in pycspr.types.TYPES_SIMPLE:
            cl_type_t0 = pycspr.cl_type_factory.simple(type_key_t0)
            cl_type_t1 = pycspr.cl_type_factory.simple(type_key_t1)
            cl_type_t2 = pycspr.cl_type_factory.simple(type_key_t2)
            cl_type = pycspr.cl_type_factory.tuple_3(cl_type_t0, cl_type_t1, cl_type_t2)
            _assert_arg(vector["value"], cl_type)


def _assert_arg(value, cl_type):
    cl_value = pycspr.cl_value.create(value, cl_type)
    arg_name = f"a-{cl_type.type_key.name.lower()}-arg"
    arg = pycspr.create_deploy_arg(arg_name, cl_value)
    assert isinstance(arg, pycspr.types.ExecutionArgument)

    # Assert optional arg can be instantiated.
    # cl_type = pycspr.factory.create_cl_type_of_option(cl_type)
    # for value in [value, None]:
    #     arg = pycspr.factory.create_deploy_arg(
    #         f"{arg_name}-optional",
    #         cl_type,
    #         value
    #         )
    #     assert isinstance(arg, pycspr.types.ExecutionArgument)
