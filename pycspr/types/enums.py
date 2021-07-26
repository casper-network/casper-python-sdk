import enum



class CLTypeKey(enum.Enum):
    """Enumeration over set of CL types.
    
    """
    BOOL = 0
    I32 = 1
    I64 = 2
    U8 = 3
    U32 = 4
    U64 = 5
    U128 = 6
    U256 = 7
    U512 = 8
    UNIT = 9
    STRING = 10
    KEY = 11
    UREF = 12
    OPTION = 13
    LIST = 14
    BYTE_ARRAY = 15
    RESULT = 16
    MAP = 17
    TUPLE_1 = 18
    TUPLE_2 = 19
    TUPLE_3 = 20
    ANY = 21
    PUBLIC_KEY = 22


class CLAccessRights(enum.Enum):
    """Enumeration over set of CL storage item access rights.
    
    """
    NONE = 0
    READ = 1
    WRITE = 2
    ADD = 4
    READ_WRITE = 3
    READ_ADD = 5
    ADD_WRITE = 6
    READ_ADD_WRITE = 7


class NodeSseChannelType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.
    
    """
    deploys = enum.auto()
    main = enum.auto()
    sigs = enum.auto()


class NodeSseEventType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.
    
    """
    ApiVersion = enum.auto()
    BlockAdded = enum.auto()
    DeployAccepted = enum.auto()
    DeployProcessed = enum.auto()
    Fault = enum.auto()
    FinalitySignature = enum.auto()
    Step = enum.auto()


# Set of types considered to be numeric.
TYPES_NUMERIC = {
    CLTypeKey.I32,
    CLTypeKey.I64,
    CLTypeKey.U8,
    CLTypeKey.U32,
    CLTypeKey.U64,
    CLTypeKey.U128,
    CLTypeKey.U256,
    CLTypeKey.U512,
}


# Set of types considered to be simple.
TYPES_SIMPLE = {
    CLTypeKey.BOOL,
    CLTypeKey.I32,
    CLTypeKey.I64,
    CLTypeKey.KEY,
    CLTypeKey.PUBLIC_KEY,
    CLTypeKey.STRING,
    CLTypeKey.U8,
    CLTypeKey.U32,
    CLTypeKey.U64,
    CLTypeKey.U128,
    CLTypeKey.U256,
    CLTypeKey.U512,
    CLTypeKey.UNIT,
    CLTypeKey.UREF,
}
