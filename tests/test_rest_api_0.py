import pycspr

from pycspr import NodeRestClient


# def test_get_chain_spec(REST_CLIENT: pycspr.NodeClient):
#     def _assert(response):
#         assert isinstance(response, dict)
#         assert len(response) == 3
#         assert "chainspec_bytes" in response
#         assert "maybe_genesis_accounts_bytes" in response
#         assert "maybe_global_state_bytes" in response

#     _assert(REST_CLIENT.get_chain_spec())


def test_get_node_metrics(REST_CLIENT: NodeRestClient):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_metrics.json
        assert isinstance(response, list)
        assert len(response) > 300

    _assert(REST_CLIENT.get_node_metrics())


def test_get_node_metric(REST_CLIENT: NodeRestClient):
    def _assert(response):
        # e.g. docs/api_reponses/rest_metrics.json
        assert isinstance(response, list)
        assert len(response) == 1

    _assert(REST_CLIENT.get_node_metric("mem_deploy_gossiper"))
