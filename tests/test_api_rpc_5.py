from pycspr import NodeRpcClient
from pycspr.types.node.rpc import GlobalStateID
from pycspr.types.node.rpc import PurseID
from pycspr.types.node.rpc import PurseIDType
from pycspr.types.node.rpc import URef


async def test_get_account_balance_under_purse_uref(
    RPC_CLIENT: NodeRpcClient,
    account_main_purse_uref: URef,
    global_state_id: GlobalStateID
):
    purse_id = PurseID(account_main_purse_uref, PurseIDType.UREF)
    data = await RPC_CLIENT.get_account_balance(purse_id, global_state_id)

    assert isinstance(data, int)
    assert data >= 0


async def test_get_account_balance_under_account_hash(
    RPC_CLIENT: NodeRpcClient,
    account_hash: bytes,
    global_state_id: GlobalStateID
):
    purse_id = PurseID(account_hash, PurseIDType.ACCOUNT_HASH)
    data = await RPC_CLIENT.get_account_balance(purse_id, global_state_id)

    assert isinstance(data, int)
    assert data >= 0


async def test_get_account_balance_under_account_key(
    RPC_CLIENT: NodeRpcClient,
    account_key: bytes,
    global_state_id: GlobalStateID
):
    purse_id = PurseID(account_key, PurseIDType.PUBLIC_KEY)
    data = await RPC_CLIENT.get_account_balance(purse_id, global_state_id)

    assert isinstance(data, int)
    assert data >= 0
