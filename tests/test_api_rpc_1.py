from pycspr import NodeRpcClient
from pycspr.api.constants import RPC_ENDPOINTS


def test_get_rpc_schema(RPC_CLIENT: NodeRpcClient):
    data = RPC_CLIENT.get_rpc_schema()

    assert isinstance(data, dict)
    assert "openrpc" in data


def test_get_rpc_endpoints(RPC_CLIENT: NodeRpcClient):
    data = RPC_CLIENT.get_rpc_endpoints()

    assert isinstance(data, list)
    assert data == sorted(RPC_ENDPOINTS)


def test_get_rpc_endpoint(RPC_CLIENT: NodeRpcClient):
    for endpoint in RPC_ENDPOINTS:
        data = RPC_CLIENT.get_rpc_endpoint(endpoint)
        assert isinstance(data, dict)


def test_get_chainspec(RPC_CLIENT: NodeRpcClient):
    data = RPC_CLIENT.get_chainspec()

    assert isinstance(data, dict)
    assert "chainspec_bytes" in data
    assert "maybe_genesis_accounts_bytes" in data
    assert "maybe_global_state_bytes" in data
