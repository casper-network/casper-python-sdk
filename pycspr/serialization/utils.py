import enum
import typing



# Custom type representing a single unsigned 8 bit integer, i.e. a Byte.
Byte = typing.NewType("Unsigned 8 bit integer", int)

# Custom type representing an array of unsigned 8 bit integers.
ByteArray = typing.List[Byte]

# Custom type representing a stream of bytes.
ByteStream = typing.NewType("Byte stream", bytes)

# Custom type representing an array of unsigned 8 bit integers.
HexString = typing.NewType("Hexadecimal string", str)


class CLType(enum.Enum):
    """Enumeration over set of supported CL types.
    
    """
    # --------------------------------
    # Primitive types.
    # --------------------------------

    BOOL = 0
    I32 = 1
    I64 = 2
    U8 = 3
    U32 = 4
    U64 = 5
    U128 = 6
    U256 = 7
    U512 = 8

    # --------------------------------
    # String + variants.
    # --------------------------------

    UNIT = 9
    STRING = 10
    # KEY = 11

    # UREF = 12
    # PUBLIC_KEY = 22
    # ACCOUNT_HASH = 23 # ???

    # --------------------------------
    # Complex.
    # --------------------------------

    # OPTION = 13
    # LIST = 14
    # BYTE_ARRAY = 15
    # RESULT = 16
    # MAP = 17
    # TUPLE_1 = 18
    # TUPLE_2 = 19
    # TUPLE_3 = 20
    # ANY = 21


class CLEncoding(enum.Enum):
    """Enumeration over set of supported value encodings.
    
    """
    BYTE_ARRAY = enum.auto()
    BYTE_STREAM = enum.auto()
    HEX_STRING = enum.auto()


class DecoderError(Exception):
    """Raised whenever domain type instance decoding fails.

    """
    def __init__(self, typeof: CLType, msg: str):
        """Object constructor.

        """
        super(DecoderError, self).__init__(f"{typeof} :: {msg}")


class EncoderError(Exception):
    """Raised whenever domain type instance encoding fails.

    """
    def __init__(self, typeof: CLType, msg: str):
        """Object constructor.

        """
        super(EncoderError, self).__init__(f"{typeof} :: {msg}")


def int_to_le_bytes(x: int, length: int, signed: bool):
    """Converts an integer to a little endian byte array.
    
    """
    return [i for i in x.to_bytes(length, 'little', signed=signed)]
    return [0xff & x >> 8 * i for i in range(length)]


def int_from_le_bytes(bytes, signed: bool):
    """Converts a little endian byte array to an integer.
    
    """
    return int.from_bytes(bytes, 'little', signed=signed)
