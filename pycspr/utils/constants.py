import collections

from pycspr.types import CLTypeKey



# Data structure representing numerical constraints.
NumericConstraints = collections.namedtuple("NumericConstraints", ["LENGTH", "MIN", "MAX"])

# Map: numerical type <-> constraints.
NUMERIC_CONSTRAINTS ={
    CLTypeKey.I32: NumericConstraints(4, -(2 ** 32), (2 ** 32) - 1),
    CLTypeKey.I64: NumericConstraints(8, -(2 ** 64), (2 ** 64) - 1),
    CLTypeKey.U8: NumericConstraints(1, 0, (2 ** 8) - 1),
    CLTypeKey.U32: NumericConstraints(4, 0, (2 ** 32) - 1),
    CLTypeKey.U64: NumericConstraints(8, 0, (2 ** 64) - 1),
    CLTypeKey.U128: NumericConstraints(16, 0, (2 ** 128) - 1),
    CLTypeKey.U256: NumericConstraints(32, 0, (2 ** 256) - 1),
    CLTypeKey.U512: NumericConstraints(64, 0, (2 ** 512) - 1)
}

# Default number of motes to pay for standard payments.
STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS = 1e4

# Default deploy time to live.
DEFAULT_DEPLOY_TTL = "1day"

# Default deploy gas price.
DEFAULT_GAS_PRICE = 1
