import pathlib

from pycctl.constants import ASSYMETRIC_KEY_FNAME
from pycctl.env import EVarType
from pycctl.env import get_evar
from pycctl.types import AccountType
from pycctl.types import AssymetricKeyType


def get_path_to_root() -> pathlib.Path:
    return pathlib.Path(get_evar(EVarType.CCTL))


def get_path_to_assets() -> pathlib.Path:
    return get_path_to_root() / "assets"


def get_path_to_binary(fname: str = None) -> pathlib.Path:
    if fname is None:
        return get_path_to_assets() / "bin"
    else:
        return get_path_to_assets() / "bin" / fname


def get_path_to_account_private_key(account_type: AccountType, account_idx: int = 1):
    return get_path_to_account_key(account_type, AssymetricKeyType.PRIVATE, account_idx)


def get_path_to_account_public_key(account_type: AccountType, account_idx: int = 1):
    return get_path_to_account_key(account_type, AssymetricKeyType.PUBLIC, account_idx)


def get_path_to_account_directory(account_type: AccountType, account_idx: int = 1) -> pathlib.Path:
    if account_type == AccountType.FAUCET:
        return get_path_to_assets() / "faucet"
    elif account_type == AccountType.USER:
        return get_path_to_assets() / "users" / f"user-{account_idx}"
    elif account_type == AccountType.VALIDATOR:
        return get_path_to_assets() / "nodes" / f"node-{account_idx}"
    else:
        raise ValueError("Invalid account type")


def get_path_to_account_key_directory(account_type: AccountType, account_idx: int = 1) -> pathlib.Path:
    if account_type in {AccountType.FAUCET, AccountType.USER}:
        return get_path_to_account_directory(account_type, account_idx)
    elif account_type == AccountType.VALIDATOR:
        return get_path_to_account_directory(account_type, account_idx) / "keys"
    else:
        raise ValueError("Invalid account type")


def get_path_to_account_key(account_type: AccountType, key_type: AssymetricKeyType, account_idx: int = 1) -> pathlib.Path:
    return get_path_to_account_key_directory(account_type, account_idx) / ASSYMETRIC_KEY_FNAME[key_type]


def get_path_to_faucet() -> pathlib.Path:
    return get_path_to_account_directory(AccountType.FAUCET)


def get_path_to_genesis_accounts() -> pathlib.Path:
    return get_path_to_assets() / "genesis" / "accounts.toml"


def get_path_to_genesis_chainspec() -> pathlib.Path:
    return get_path_to_assets() / "genesis" / "chainspec.toml"


def get_path_to_node(node_idx: int) -> pathlib.Path:
    return get_path_to_account_directory(AccountType.VALIDATOR, node_idx)


def get_path_to_node_config(node_idx: int, fname: str) -> pathlib.Path:
    return get_path_to_node(node_idx) / "config" / fname


def get_path_to_user(user_idx: int) -> pathlib.Path:
    return get_path_to_account_directory(AccountType.USER, user_idx)


def read_account_public_key(account_type: AccountType, account_idx: int = 1) -> bytes:
    return bytes.fromhex(_read_file(
        get_path_to_account_key(account_type, AssymetricKeyType.PUBLIC, account_idx)
    ))


def read_account_private_key(account_type: AccountType, account_idx: int = 1) -> str:
    return _read_file(
        get_path_to_account_key(account_type, AssymetricKeyType.PRIVATE, account_idx)
    )


def _read_file(fpath: pathlib.Path) -> str:
    with open(fpath, 'r') as fstream:
        return fstream.read()
