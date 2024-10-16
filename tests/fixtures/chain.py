import pytest

from pycspr import NodeBinaryClient
from pycspr.type_defs.crypto import DigestBytes
from pycspr.types.node import AccountKey
from pycspr.types.node import Block
from pycspr.types.node import GlobalStateID
from pycspr.types.node import GlobalStateIDType
from pycspr.types.node import StateRootHash
from pycspr.types.node import URef
from pycspr.type_defs.chain import BlockHeader


@pytest.fixture(scope="session")
async def account_main_purse_uref(
    NODE_BINARY_CLIENT: NodeBinaryClient,
    account_key: AccountKey
) -> URef:
    """Returns an on-chain account's main purse unforgeable reference.

    """
    pass


@pytest.fixture(scope="session")
async def block(NODE_BINARY_CLIENT: NodeBinaryClient) -> Block:
    """Returns most recent block.

    """
    pass


@pytest.fixture(scope="session")
async def block_hash(block: Block) -> DigestBytes:
    """Returns hash of most recent block.

    """
    pass


@pytest.fixture(scope="session")
async def BLOCK_HEADER(NODE_BINARY_CLIENT: NodeBinaryClient) -> BlockHeader:
    """Returns most recent block.

    """
    request_id = random.randint(0, int(1e2))
    response = await NODE_BINARY_CLIENT.information.get_block_header(request_id)

    return response.payload


@pytest.fixture(scope="session")
def global_state_id(state_root_hash: StateRootHash) -> GlobalStateID:
    """Returns current state root hash.

    """
    pass


@pytest.fixture(scope="session")
async def state_root_hash(NODE_BINARY_CLIENT: NodeBinaryClient) -> StateRootHash:
    """Returns current state root hash.

    """
    pass


@pytest.fixture(scope="session")
async def switch_block(NODE_BINARY_CLIENT: NodeBinaryClient) -> dict:
    """Returns hash of most recent switch block.

    """
    pass


@pytest.fixture(scope="session")
async def switch_block_hash(switch_block: Block) -> DigestBytes:
    """Returns hash of most recent switch block.

    """
    pass
