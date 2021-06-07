def test_bool(LIB):
    values = (False, True, 0, 1)

    _assert_round_trip(LIB, LIB.CLType.BOOL, values)


def test_i32(LIB):
    values = (-(2 ** 31), 0, (2 ** 31) - 1)

    _assert_round_trip(LIB, LIB.CLType.I32, values)


def test_i64(LIB):
    values = (-(2 ** 63), 0, (2 ** 63) - 1)

    _assert_round_trip(LIB, LIB.CLType.I64, values)


def test_string(LIB):
    values = ("test_测试", "")

    _assert_round_trip(LIB, LIB.CLType.STRING, values)


def test_u8(LIB):
    values = (0, 255)

    _assert_round_trip(LIB, LIB.CLType.U8, values)


def test_u32(LIB):
    values = (0, (2 ** 32) - 1)

    _assert_round_trip(LIB, LIB.CLType.U32, values)


def test_u64(LIB):
    values = (0, (2 ** 64) - 1)

    _assert_round_trip(LIB, LIB.CLType.U64, values)


def test_u128(LIB):
    values = (0, (2 ** 128) - 1)

    _assert_round_trip(LIB, LIB.CLType.U128, values)


def test_u256(LIB):
    values = (0, (2 ** 256) - 1)

    _assert_round_trip(LIB, LIB.CLType.U256, values)


def test_u512(LIB):
    values = (0, (2 ** 512) - 1)

    _assert_round_trip(LIB, LIB.CLType.U512, values)


def test_unit(LIB):
    values = (None, )

    _assert_round_trip(LIB, LIB.CLType.UNIT, values)


def _assert_round_trip(LIB, typeof, values):
    """Performs round trip serialisation assertion.
    
    """
    for encoding in LIB.CLEncoding:
        for value in values:
            encoded = LIB.encode(typeof, value, encoding)
            decoded = LIB.decode(encoded, encoding)
            assert value == decoded
