from pycctl.accounts import get_account_balance
from pycctl.constants import NET_BINARIES
from pycctl.constants import NODE_CONFIG
from pycctl.constants import NODE_COUNT
from pycctl.constants import USER_COUNT
from pycctl.types import AccountType
from pycctl.types import AssymetricKeyType
from pycctl.fsys import get_path_to_account_key
from pycctl.fsys import get_path_to_account_key_directory
from pycctl.fsys import get_path_to_assets
from pycctl.fsys import get_path_to_binary
from pycctl.fsys import get_path_to_genesis_accounts
from pycctl.fsys import get_path_to_genesis_chainspec
from pycctl.fsys import get_path_to_node
from pycctl.fsys import get_path_to_node_config
from pycctl.fsys import get_path_to_root
from pycctl.node import get_rpc_client


def validate_chain_accounts_are_funded():
    assert get_account_balance(AccountType.FAUCET) > 0
    for idx in range(1, USER_COUNT):
        assert get_account_balance(AccountType.USER, idx) > 0
    for idx in range(1, NODE_COUNT):
        assert get_account_balance(AccountType.VALIDATOR, idx) > 0


def validate_infra_net_assets_setup():
    """Validates that net infrastructure assets are correctly setup.
    
    """
    def _parse_path_to_root():
        assert get_path_to_root().exists()

    def _parse_path_to_assets():
        assert get_path_to_assets().exists()

    def _parse_path_to_account_directory():
        for account_type in AccountType:
            if account_type == AccountType.FAUCET:
                assert get_path_to_account_key_directory(account_type).exists()
            elif account_type == AccountType.USER:
                for idx in range(1, USER_COUNT):
                    assert get_path_to_account_key_directory(account_type, idx).exists()
            elif account_type == AccountType.VALIDATOR:
                for idx in range(1, NODE_COUNT):
                    assert get_path_to_account_key_directory(account_type, idx).exists()

    def _parse_path_to_account_directory_keys():
        for account_type in AccountType:
            for key_type in AssymetricKeyType:
                if account_type == AccountType.FAUCET:
                    assert get_path_to_account_key(account_type, key_type).exists()
                elif account_type == AccountType.USER:
                    for idx in range(1, USER_COUNT):
                        assert get_path_to_account_key(account_type, key_type, idx).exists()
                elif account_type == AccountType.VALIDATOR:
                    for idx in range(1, NODE_COUNT):
                        assert get_path_to_account_key(account_type, key_type, idx).exists()

    def _parse_path_to_genesis_artefacts():
        assert get_path_to_genesis_accounts().exists()
        assert get_path_to_genesis_chainspec().exists()

    def _parse_path_to_net_binaries():
        for fname in NET_BINARIES:
            assert get_path_to_binary(fname).exists()

    def _parse_path_to_node():
        for idx in range(1, NODE_COUNT):
            assert get_path_to_node(idx).exists()
            for fname in NODE_CONFIG:
                assert get_path_to_node_config(idx, fname).exists()

    for func in {
        _parse_path_to_root,
        _parse_path_to_assets,
        _parse_path_to_account_directory,
        _parse_path_to_account_directory_keys,
        _parse_path_to_genesis_artefacts,
        _parse_path_to_net_binaries,
        _parse_path_to_node,
    }:
        func()


def validate_infra_net_is_up():
    """Validates that net nodes are up.
    
    """
    count_up: int = 0
    for idx in range(1, NODE_COUNT):
        if validate_infra_node_start(idx):
            count_up += 1

    assert count_up >= int(NODE_COUNT / 2), count_up


def validate_infra_node_start(idx: int) -> bool:
    """Validates that node is up.
    
    """
    client = get_rpc_client(idx)        
    try:
        client.get_node_status()
    except:
        return False
    else:
        return True
