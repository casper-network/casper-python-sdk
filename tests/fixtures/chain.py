import pytest

from pycspr import NodeRpcClient
from pycspr.crypto.types import DigestBytes
from pycspr.types.node import AccountKey
from pycspr.types.node import Block
from pycspr.types.node import GlobalStateID
from pycspr.types.node import GlobalStateIDType
from pycspr.types.node import StateRootHash
from pycspr.types.node import URef


@pytest.fixture(scope="session")
async def account_main_purse_uref(
    SIDECAR_RPC_CLIENT: NodeRpcClient,
    account_key: AccountKey
) -> URef:
    """Returns an on-chain account's main purse unforgeable reference.

    """
    return await SIDECAR_RPC_CLIENT.get_account_main_purse_uref(account_key)


@pytest.fixture(scope="session")
async def block(SIDECAR_RPC_CLIENT: NodeRpcClient) -> Block:
    """Returns most recent block.

    """
    return await SIDECAR_RPC_CLIENT.get_block()


@pytest.fixture(scope="session")
async def block_hash(block: Block) -> DigestBytes:
    """Returns hash of most recent block.

    """
    return block.hash


@pytest.fixture(scope="session")
def global_state_id(state_root_hash: StateRootHash) -> GlobalStateID:
    """Returns current state root hash.

    """
    return GlobalStateID(state_root_hash, GlobalStateIDType.STATE_ROOT_HASH)


@pytest.fixture(scope="session")
async def state_root_hash(SIDECAR_RPC_CLIENT: NodeRpcClient) -> StateRootHash:
    """Returns current state root hash.

    """
    return await SIDECAR_RPC_CLIENT.get_state_root_hash()


@pytest.fixture(scope="session")
async def switch_block(SIDECAR_RPC_CLIENT: NodeRpcClient) -> dict:
    """Returns hash of most recent switch block.

    """
    return await SIDECAR_RPC_CLIENT.get_block_at_era_switch()


@pytest.fixture(scope="session")
async def switch_block_hash(switch_block: Block) -> DigestBytes:
    """Returns hash of most recent switch block.

    """
    return switch_block.hash
