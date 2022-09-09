from pycspr.api.constants import RPC_ENDPOINTS
from pycspr.api.constants import RPC_INFO_GET_CHAINSPEC

def test_get_rpc_schema(CLIENT):
    def _assert(response):
        assert isinstance(response, dict)
        assert "openrpc" in response

    _assert(CLIENT.get_rpc_schema())


def test_get_rpc_endpoints(CLIENT):
    def _assert(response):
        assert isinstance(response, list)
        assert response == sorted(RPC_ENDPOINTS)

    _assert(CLIENT.get_rpc_endpoints())


def test_get_rpc_endpoint(CLIENT):
    def _assert(response):
        assert isinstance(response, dict)

    for endpoint in RPC_ENDPOINTS:
        _assert(CLIENT.get_rpc_endpoint(endpoint))


def test_get_chain_spec(CLIENT):
    def _assert(response):
        assert isinstance(response, dict)
        for field in (
            "chainspec_bytes",
            "maybe_genesis_accounts_bytes",
            "maybe_global_state_bytes"
            ):
            assert field in response
            assert "chainspec_bytes" in response
    _assert(CLIENT.get_chain_spec())
