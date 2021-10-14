import pytest



@pytest.fixture(scope="session")
def account_main_purse_uref(CLIENT, account_key: bytes) -> str:
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
def state_root_hash(CLIENT) -> bytes:
    """Returns current state root hash. 
    
    """
    return CLIENT.get_state_root_hash()


@pytest.fixture(scope="session")
def switch_block(CLIENT) -> str:
    """Returns hash of most recent switch block. 
    
    """
    return CLIENT.get_block_at_era_switch()


@pytest.fixture(scope="session")
def switch_block_hash(switch_block) -> str:
    """Returns hash of most recent switch block. 
    
    """
    return switch_block["hash"]
