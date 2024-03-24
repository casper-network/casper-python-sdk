import pytest

from pycspr import NodeRpcClient
from pycspr.types.cl import CLV_URef
from pycspr.types.api.rpc import GlobalStateID
from pycspr.types.api.rpc import GlobalStateIDType


@pytest.fixture(scope="session")
def account_main_purse_uref(RPC_CLIENT: NodeRpcClient, account_key: bytes) -> CLV_URef:
    """Returns an on-chain account's main purse unforgeable reference.

    """
    return RPC_CLIENT.get_account_main_purse_uref(account_key)


@pytest.fixture(scope="session")
def block(RPC_CLIENT: NodeRpcClient) -> dict:
    """Returns most recent block.

    """
    return RPC_CLIENT.get_block()


@pytest.fixture(scope="session")
def block_hash(block) -> str:
    """Returns hash of most recent block.

    """
    return block["hash"]


@pytest.fixture(scope="session")
def global_state_id(state_root_hash) -> GlobalStateID:
    """Returns current state root hash.

    """
    return GlobalStateID(state_root_hash, GlobalStateIDType.STATE_ROOT_HASH)


@pytest.fixture(scope="session")
def state_root_hash(RPC_CLIENT: NodeRpcClient) -> bytes:
    """Returns current state root hash.

    """
    return RPC_CLIENT.get_state_root_hash()


@pytest.fixture(scope="session")
def switch_block(RPC_CLIENT: NodeRpcClient) -> dict:
    """Returns hash of most recent switch block.

    """
    return RPC_CLIENT.get_block_at_era_switch()


@pytest.fixture(scope="session")
def switch_block_hash(switch_block) -> str:
    """Returns hash of most recent switch block.

    """
    return switch_block["hash"]
