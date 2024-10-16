# Default tx time to live.
DEFAULT_TX_TTL = "5m"

# Default tx gas price.
DEFAULT_TX_GAS_PRICE = 1

# Default tx gas price tolerance.
DEFAULT_TX_GAS_PRICE_TOLERANCE = 1

# Maximum deploy time to live = 2 hours.
TX_MAX_TTL_MS = 1000 * 60 * 60 * 2

# Maximum value of a transfer ID.
MAX_TRANSFER_ID = (2 ** 63) - 1

# Minimum amount in motes of a wasmless transfer.
MIN_TRANSFER_AMOUNT_MOTES = 2_500_000_000

# Millisecond durations of relevance.
MS_1_SECOND: int = 1000
MS_1_MINUTE: int = 60 * MS_1_SECOND
MS_1_HOUR: int = 60 * MS_1_MINUTE

# Default number of motes to pay for standard payments.
STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS = int(1e8)

# Default number of motes to pay for standard delegation.
STANDARD_PAYMENT_FOR_DELEGATION = int(5e9)

# Default number of motes to pay for standard delegation withdrawal.
STANDARD_PAYMENT_FOR_DELEGATION_WITHDRAWAL = int(5e9)

# Default number of motes to pay for standard auction bid.
STANDARD_PAYMENT_FOR_AUCTION_BID = int(5e9)

# Default number of motes to pay for standard auction bid withdrawal.
STANDARD_PAYMENT_FOR_AUCTION_BID_WITHDRAWAL = int(5e9)
