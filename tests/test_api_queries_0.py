from pycspr.api.constants import RPC_ENDPOINTS



def test_get_rpc_schema(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, dict)
        assert "openrpc" in response

    _assert(CLIENT.get_rpc_schema())


def test_get_rpc_endpoints(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, list)
        assert response == sorted(RPC_ENDPOINTS)

    _assert(CLIENT.get_rpc_endpoints())


def test_get_rpc_endpoint(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, dict)        

    for endpoint in RPC_ENDPOINTS:
        _assert(CLIENT.get_rpc_endpoint(endpoint))
