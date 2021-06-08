def _assert_round_trip(LIB, typeof, values):
    """Performs round trip serialisation assertion.
    
    """
    for encoding in LIB.CLEncoding:
        for value in values:
            encoded = LIB.encode(typeof, value, encoding)
            decoded = LIB.decode(encoded, encoding)
            assert value == decoded

            print(value, encoded, decoded)


def test_bool(LIB):
    values = (False, True, 0, 1)

    _assert_round_trip(LIB, LIB.CLTypeKey.BOOL, values)


def test_i32(LIB):
    values = (-(2 ** 31), 0, (2 ** 31) - 1)

    _assert_round_trip(LIB, LIB.CLTypeKey.I32, values)


def test_i64(LIB):
    values = (-(2 ** 63), 0, (2 ** 63) - 1)

    _assert_round_trip(LIB, LIB.CLTypeKey.I64, values)


def test_string(LIB):
    values = ("test_测试", "")

    _assert_round_trip(LIB, LIB.CLTypeKey.STRING, values)


def test_u8(LIB):
    values = (0, 255)

    _assert_round_trip(LIB, LIB.CLTypeKey.U8, values)


def test_u32(LIB):
    values = (0, (2 ** 32) - 1)

    _assert_round_trip(LIB, LIB.CLTypeKey.U32, values)


def test_u64(LIB):
    values = (0, (2 ** 64) - 1)
    values = (1,)

    _assert_round_trip(LIB, LIB.CLTypeKey.U64, values)

    # raise NotImplementedError()


def test_u128(LIB):
    values = (0, (2 ** 128) - 1)

    _assert_round_trip(LIB, LIB.CLTypeKey.U128, values)


def test_u256(LIB):
    values = (0, (2 ** 256) - 1)

    _assert_round_trip(LIB, LIB.CLTypeKey.U256, values)


def test_u512(LIB):
    values = (0, (2 ** 512) - 1, 3618733144750325837958790227950415868742292184814728655972723411435898710232007994755759630545001033316379250637667110010115434549409256374699329574956472)
    values = (2500000000,)
    values = (1000000000 , 123456789, 10000000000000)

    _assert_round_trip(LIB, LIB.CLTypeKey.U512, values)

    # raise NotImplementedError()


def test_unit(LIB):
    values = (None, )

    _assert_round_trip(LIB, LIB.CLTypeKey.UNIT, values)
