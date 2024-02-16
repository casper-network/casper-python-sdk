import pytest

from pycspr.types import CL_URef
from pycspr.types import GlobalStateID
from pycspr.types import GlobalStateIDType


@pytest.fixture(scope="session")
def account_main_purse_uref(CLIENT, account_key: bytes) -> CL_URef:
    """Returns an on-chain account's main purse unforgeable reference.

    """
    return CLIENT.get_account_main_purse_uref(account_key)


@pytest.fixture(scope="session")
def block(CLIENT) -> dict:
    """Returns most recent block.

    """
    return CLIENT.get_block()


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
def state_root_hash(CLIENT) -> bytes:
    """Returns current state root hash.

    """
    return CLIENT.get_state_root_hash()


@pytest.fixture(scope="session")
def switch_block(CLIENT) -> dict:
    """Returns hash of most recent switch block.

    """
    return CLIENT.get_block_at_era_switch()


@pytest.fixture(scope="session")
def switch_block_hash(switch_block) -> str:
    """Returns hash of most recent switch block.

    """
    return switch_block["hash"]
