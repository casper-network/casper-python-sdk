from pycspr import NodeRpcClient
from pycspr.types.cl import CLV_URef
from pycspr.types.cl import CLV_URefAccessRights
from pycspr.types.node.rpc import AccountInfo


async def test_get_state_root(RPC_CLIENT: NodeRpcClient):
    def _assert(response):
        assert isinstance(response, bytes)
        assert len(response) == 32

    for block_id in (None, 1):
        _assert(await RPC_CLIENT.get_state_root_hash(block_id))


async def test_get_account_info(RPC_CLIENT: NodeRpcClient, account_key: bytes):
    data: dict = await RPC_CLIENT.get_account_info(account_key, decode=False)
    assert isinstance(data, dict)

    data: AccountInfo = await RPC_CLIENT.get_account_info(account_key, decode=True)
    assert isinstance(data, AccountInfo)


async def test_get_account_main_purse_uref(RPC_CLIENT: NodeRpcClient, account_key: bytes):
    def _assert(response):
        # e.g. uref-827d5984270fed5aaaf076e1801733414a307ed8c5d85cad8ebe6265ba887b3a-007
        assert isinstance(response, CLV_URef)
        assert len(response.address) == 32
        assert response.access_rights == CLV_URefAccessRights.READ_ADD_WRITE

    _assert(await RPC_CLIENT.get_account_main_purse_uref(account_key))
