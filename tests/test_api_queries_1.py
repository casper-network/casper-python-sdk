def test_get_node_metrics(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_metrics.json
        assert isinstance(response, list)
        assert len(response) > 300

    _assert(CLIENT.get_node_metrics())


def test_get_node_metric(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rest_metrics.json
        assert isinstance(response, list)
        assert len(response) == 1

    _assert(CLIENT.get_node_metric("mem_deploy_gossiper"))


def test_get_node_peers(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_info_get_peers.json
        assert isinstance(response, list)

    _assert(CLIENT.get_node_peers())


def test_get_node_status(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_info_get_status.json
        assert isinstance(response, dict)

    _assert(CLIENT.get_node_status())


def test_get_validator_changes(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_info_get_status.json
        assert isinstance(response, list)

    _assert(CLIENT.get_validator_changes())
