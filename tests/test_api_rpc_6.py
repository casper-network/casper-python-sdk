from pycspr import NodeRpcClient
from pycspr.types.cl import CLV_URef
from pycspr.types.cl import CLV_URefAccessRights
from pycspr.types.node.rpc import AccountInfo
from pycspr.types.node.rpc import URef
from pycspr.types.node.rpc import URefAccessRights


async def test_get_state_root(RPC_CLIENT: NodeRpcClient):
    def _assert(response):
        assert isinstance(response, bytes)
        assert len(response) == 32

    for block_id in (None, 1):
        _assert(await RPC_CLIENT.get_state_root_hash(block_id))


async def test_get_account_info_1(RPC_CLIENT: NodeRpcClient, account_key: bytes):
    data: dict = await RPC_CLIENT.get_account_info(account_key, decode=False)
    assert isinstance(data, dict)


async def test_get_account_info_2(RPC_CLIENT: NodeRpcClient, account_key: bytes):
    data: AccountInfo = await RPC_CLIENT.get_account_info(account_key, decode=True)
    assert isinstance(data, AccountInfo)


async def test_get_account_main_purse_uref(RPC_CLIENT: NodeRpcClient, account_key: bytes):
    data: URef = await RPC_CLIENT.get_account_main_purse_uref(account_key)
    assert isinstance(data, URef)
    assert len(data.address) == 32
    assert data.access_rights == URefAccessRights.READ_ADD_WRITE
