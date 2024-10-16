from pycspr import NodeRpcClient
from pycspr.types.node import AccountInfo
from pycspr.types.node import URef
from pycspr.types.node import URefAccessRights


async def test_get_state_root(SIDECAR_RPC_CLIENT: NodeRpcClient):
    def _assert(response):
        assert isinstance(response, bytes)
        assert len(response) == 32

    for block_id in (None, 1):
        _assert(await SIDECAR_RPC_CLIENT.get_state_root_hash(block_id))


async def test_get_account_info_1(SIDECAR_RPC_CLIENT: NodeRpcClient, account_key: bytes):
    data: dict = await SIDECAR_RPC_CLIENT.get_account_info(account_key, decode=False)
    assert isinstance(data, dict)


async def test_get_account_info_2(SIDECAR_RPC_CLIENT: NodeRpcClient, account_key: bytes):
    data: AccountInfo = await SIDECAR_RPC_CLIENT.get_account_info(account_key, decode=True)
    assert isinstance(data, AccountInfo)


async def test_get_account_main_purse_uref(SIDECAR_RPC_CLIENT: NodeRpcClient, account_key: bytes):
    data: URef = await SIDECAR_RPC_CLIENT.get_account_main_purse_uref(account_key)
    assert isinstance(data, URef)
    assert len(data.address) == 32
    assert data.access_rights == URefAccessRights.READ_ADD_WRITE
