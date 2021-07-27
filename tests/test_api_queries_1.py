def test_get_node_metrics(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_metrics.json
        assert isinstance(response, list)
        assert len(response) > 300

    _assert(CLIENT.queries.get_node_metrics())


def test_get_node_metric(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rest_metrics.json
        assert isinstance(response, list)
        assert len(response) == 1

    _assert(CLIENT.queries.get_node_metric("mem_deploy_gossiper"))


def test_get_node_peers(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_info_get_peers.json
        assert isinstance(response, list)

    _assert(CLIENT.queries.get_node_peers())


def test_get_node_status(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_info_get_status.json
        assert isinstance(response, dict)

    _assert(CLIENT.queries.get_node_status())


def test_get_rpc_schema(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, dict)
        assert "openrpc" in response

    _assert(CLIENT.queries.get_rpc_schema())


def test_get_rpc_endpoints(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, list)
        print(response)
        assert response == sorted(CLIENT.NODE_RPC_ENDPOINTS)

    _assert(CLIENT.queries.get_rpc_endpoints())


def test_get_rpc_endpoint(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, dict)        

    for endpoint in CLIENT.NODE_RPC_ENDPOINTS:
        _assert(CLIENT.queries.get_rpc_endpoint(endpoint))
