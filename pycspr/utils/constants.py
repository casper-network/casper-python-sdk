import collections

from pycspr.types import CLTypeKey


# Data structure representing numerical constraints.
NumericConstraints = collections.namedtuple("NumericConstraints", ["LENGTH", "MIN", "MAX"])

# Map: numerical type <-> constraints.
NUMERIC_CONSTRAINTS = {
    CLTypeKey.I32: NumericConstraints(4, -(2 ** 32), (2 ** 32) - 1),
    CLTypeKey.I64: NumericConstraints(8, -(2 ** 64), (2 ** 64) - 1),
    CLTypeKey.U8: NumericConstraints(1, 0, (2 ** 8) - 1),
    CLTypeKey.U32: NumericConstraints(4, 0, (2 ** 32) - 1),
    CLTypeKey.U64: NumericConstraints(8, 0, (2 ** 64) - 1),
    CLTypeKey.U128: NumericConstraints(16, 0, (2 ** 128) - 1),
    CLTypeKey.U256: NumericConstraints(32, 0, (2 ** 256) - 1),
    CLTypeKey.U512: NumericConstraints(64, 0, (2 ** 512) - 1)
}


def is_outside_of_range(type_key: CLTypeKey, value: int) -> bool:
    """Returns flag indicating whether a value is outside of numeric range
       associated with the CL type.

    """
    constraints = NUMERIC_CONSTRAINTS[type_key]

    return value < constraints.MIN or value > constraints.MAX


def is_within_range(type_key: CLTypeKey, value: int) -> bool:
    """Returns flag indicating whether a value is within a numeric range associated with the CL type.

    """
    constraints = NUMERIC_CONSTRAINTS[type_key]

    return value >= constraints.MIN and value <= constraints.MAX


# Default number of motes to pay for standard payments.
STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS = int(1e9)

# Default number of motes to pay for standard delegation.
STANDARD_PAYMENT_FOR_DELEGATION = int(3e9)

# Default number of motes to pay for standard delegation withdrawal.
STANDARD_PAYMENT_FOR_DELEGATION_WITHDRAWAL = int(3e9)

# Default number of motes to pay for standard auction bid.
STANDARD_PAYMENT_FOR_AUCTION_BID = int(3e9)

# Default number of motes to pay for standard auction bid withdrawal.
STANDARD_PAYMENT_FOR_AUCTION_BID_WITHDRAWAL = int(3e9)

# Default deploy time to live.
DEFAULT_DEPLOY_TTL = "30m"

# Default deploy gas price.
DEFAULT_GAS_PRICE = 1

# Maximum deploy time to live = 1 day.
DEPLOY_TTL_MS_MAX = 1000 * 60 * 60 * 24
