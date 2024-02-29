import pycspr


def test_get_chain_spec(CLIENT: pycspr.NodeClient):
    def _assert(response):
        assert isinstance(response, dict)
        assert len(response) == 3
        assert "chainspec_bytes" in response
        assert "maybe_genesis_accounts_bytes" in response
        assert "maybe_global_state_bytes" in response

    _assert(CLIENT.get_chain_spec())


def test_get_node_metrics(CLIENT: pycspr.NodeClient):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_metrics.json
        assert isinstance(response, list)
        assert len(response) > 300

    _assert(CLIENT.get_node_metrics())


def test_get_node_metric(CLIENT: pycspr.NodeClient):
    def _assert(response):
        # e.g. docs/api_reponses/rest_metrics.json
        assert isinstance(response, list)
        assert len(response) == 1

    _assert(CLIENT.get_node_metric("mem_deploy_gossiper"))


def test_get_node_peers(CLIENT: pycspr.NodeClient):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_info_get_peers.json
        assert isinstance(response, list)

    _assert(CLIENT.get_node_peers())


def test_get_node_status(CLIENT: pycspr.NodeClient):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_info_get_status.json
        assert isinstance(response, dict)

    _assert(CLIENT.get_node_status())


def test_get_validator_changes(CLIENT: pycspr.NodeClient):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_info_get_status.json
        assert isinstance(response, list)

    _assert(CLIENT.get_validator_changes())
