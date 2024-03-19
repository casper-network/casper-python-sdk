from pycctl.types import AssymetricKeyType


ASSYMETRIC_KEY_FNAME = {
    AssymetricKeyType.PRIVATE: "secret_key.pem",
    AssymetricKeyType.PUBLIC: "public_key_hex",
}

BASE_PORT_RPC = 11100
BASE_PORT_REST = 14100
BASE_PORT_SSE = 18100
BASE_PORT_SPEC_EXEC=25100

CHAIN_NAME = "cspr-dev-cctl"

NET_BINARIES = {
    "activate_bid.wasm",
    "add_bid.wasm",
    "casper-client",
    "delegate.wasm",
    "transfer_to_account_u512.wasm",
    "undelegate.wasm",
    "withdraw_bid.wasm",
}

NODE_BINARIES = {
    "1_0_0/casper-node",
    "casper-node-launcher",
}

NODE_CONFIG = {
    "1_0_0/accounts.toml",
    "1_0_0/chainspec.toml",
    "1_0_0/config.toml",
}

NODE_COUNT = 10

SC_PAYMENT_INSTALL = int(50e9)

USER_COUNT = 10
