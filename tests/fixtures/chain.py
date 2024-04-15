import pytest

from pycspr import NodeRpcClient
from pycspr.types.crypto import DigestBytes
from pycspr.types.node.rpc import AccountKey
from pycspr.types.node.rpc import Block
from pycspr.types.node.rpc import GlobalStateID
from pycspr.types.node.rpc import GlobalStateIDType
from pycspr.types.node.rpc import StateRootHash
from pycspr.types.node.rpc import URef


@pytest.fixture(scope="session")
async def account_main_purse_uref(
    RPC_CLIENT: NodeRpcClient,
    account_key: AccountKey
) -> URef:
    """Returns an on-chain account's main purse unforgeable reference.

    """
    return await RPC_CLIENT.get_account_main_purse_uref(account_key)


@pytest.fixture(scope="session")
async def block(RPC_CLIENT: NodeRpcClient) -> Block:
    """Returns most recent block.

    """
    return await RPC_CLIENT.get_block()


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
async def state_root_hash(RPC_CLIENT: NodeRpcClient) -> StateRootHash:
    """Returns current state root hash.

    """
    return await RPC_CLIENT.get_state_root_hash()


@pytest.fixture(scope="session")
async def switch_block(RPC_CLIENT: NodeRpcClient) -> dict:
    """Returns hash of most recent switch block.

    """
    return await RPC_CLIENT.get_block_at_era_switch()


@pytest.fixture(scope="session")
async def switch_block_hash(switch_block: Block) -> DigestBytes:
    """Returns hash of most recent switch block.

    """
    return switch_block.hash
