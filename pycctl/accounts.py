from pycctl.fsys import read_account_public_key
from pycctl.node import get_rpc_client
from pycctl.types import AccountType
from pycspr import get_account_address
from pycspr.types import PurseID
from pycspr.types import PurseIDType


def get_account_balance(account_Type: AccountType, account_idx: int = None) -> int:
    key: bytes = read_account_public_key(account_Type, account_idx)
    address: bytes = get_account_address(key)
    purse_id = PurseID(address, PurseIDType.ACCOUNT_HASH)
    client = get_rpc_client()

    return client.get_account_balance(purse_id)
