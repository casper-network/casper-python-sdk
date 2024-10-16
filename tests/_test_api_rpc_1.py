from pycspr import NodeRpcClient
from pycspr.api.constants import RPC_ENDPOINTS


async def test_get_rpc_schema(SIDECAR_RPC_CLIENT: NodeRpcClient):
    data = await SIDECAR_RPC_CLIENT.get_rpc_schema()

    assert isinstance(data, dict)
    assert "openrpc" in data


async def test_get_rpc_endpoints(SIDECAR_RPC_CLIENT: NodeRpcClient):
    data = await SIDECAR_RPC_CLIENT.get_rpc_endpoints()

    assert isinstance(data, list)
    assert data == sorted(RPC_ENDPOINTS)


async def test_get_rpc_endpoint(SIDECAR_RPC_CLIENT: NodeRpcClient):
    for endpoint in RPC_ENDPOINTS:
        data = await SIDECAR_RPC_CLIENT.get_rpc_endpoint(endpoint)
        assert isinstance(data, dict)


async def test_get_chainspec(SIDECAR_RPC_CLIENT: NodeRpcClient):
    data = await SIDECAR_RPC_CLIENT.get_chainspec()

    assert isinstance(data, dict)
    for field in {
        "chainspec_bytes",
        "maybe_genesis_accounts_bytes",
        "maybe_global_state_bytes",
    }:
        assert field in data
