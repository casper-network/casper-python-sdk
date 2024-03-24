from pycspr import NodeRpcClient
from pycspr.types.cl import CLV_URef
from pycspr.types.node.rpc import GlobalStateID
from pycspr.types.node.rpc import PurseID
from pycspr.types.node.rpc import PurseIDType


def test_get_account_balance_under_purse_uref(
    RPC_CLIENT: NodeRpcClient,
    account_main_purse_uref: CLV_URef,
    global_state_id: GlobalStateID
):
    purse_id = PurseID(account_main_purse_uref, PurseIDType.UREF)
    data = RPC_CLIENT.get_account_balance(purse_id, global_state_id)

    assert isinstance(data, int)
    assert data >= 0


def test_get_account_balance_under_account_hash(
    RPC_CLIENT: NodeRpcClient,
    account_hash: bytes,
    global_state_id: GlobalStateID
):
    purse_id = PurseID(account_hash, PurseIDType.ACCOUNT_HASH)
    data = RPC_CLIENT.get_account_balance(purse_id, global_state_id)

    assert isinstance(data, int)
    assert data >= 0


def test_get_account_balance_under_account_key(
    RPC_CLIENT: NodeRpcClient,
    account_key: bytes,
    global_state_id: GlobalStateID
):
    purse_id = PurseID(account_key, PurseIDType.PUBLIC_KEY)
    data = RPC_CLIENT.get_account_balance(purse_id, global_state_id)

    assert isinstance(data, int)
    assert data >= 0
