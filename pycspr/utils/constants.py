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
DEFAULT_DEPLOY_TTL = "30m"

# Default deploy gas price.
DEFAULT_GAS_PRICE = 1

# Maximum deploy time to live = 1 day.
DEPLOY_TTL_MS_MAX = 1000 * 60 * 60 * 24

# Set of node REST endpoints.
NODE_REST_ENDPOINTS: set = {
    "metrics",
    "status",
}

# Set of node RPC endpoints.
NODE_RPC_ENDPOINTS: set = {
    'account_put_deploy',
    'chain_get_block',
    'chain_get_block_transfers',
    'chain_get_era_info_by_switch_block',
    'chain_get_state_root_hash',
    'info_get_deploy',
    'info_get_peers',
    'info_get_status',
    'state_get_account_info',
    'state_get_auction_info',
    'state_get_balance',
    'state_get_item'
    }

# Set of node SSE endpoints.
NODE_SSE_ENDPOINTS: set = {
    "main",
    "deploys",
    "sigs",
}
