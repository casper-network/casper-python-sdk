import pycspr
from pycspr.api.constants import RPC_ENDPOINTS


def test_get_rpc_schema_with_rpc_client(RPC_CLIENT: pycspr.NodeRpcClient):
    def _assert(response):
        assert isinstance(response, dict)
        assert "openrpc" in response

    _assert(RPC_CLIENT.get_rpc_schema())


def test_get_rpc_endpoints_with_rpc_client(RPC_CLIENT: pycspr.NodeRpcClient):
    def _assert(response):
        assert isinstance(response, list)
        assert response == sorted(RPC_ENDPOINTS)

    _assert(RPC_CLIENT.get_rpc_endpoints())


def test_get_rpc_endpoint_with_rpc_client(RPC_CLIENT: pycspr.NodeRpcClient):
    def _assert(response):
        assert isinstance(response, dict)

    for endpoint in RPC_ENDPOINTS:
        _assert(RPC_CLIENT.get_rpc_endpoint(endpoint))


def test_get_chainspec_with_rpc_client(RPC_CLIENT: pycspr.NodeRpcClient):
    def _assert(response):
        assert isinstance(response, dict)
        for field in (
            "chainspec_bytes",
            "maybe_genesis_accounts_bytes",
            "maybe_global_state_bytes"
            ):
            assert field in response
            assert "chainspec_bytes" in response
    _assert(RPC_CLIENT.get_chainspec())
