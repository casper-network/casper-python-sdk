def test_get_state_root_hash(CLIENT):
    def _assert(response):
        assert isinstance(response, bytes)
        assert len(response) == 32

    for block_id in (None, 1):
        _assert(CLIENT.get_state_root_hash(block_id))


def test_get_account_info(CLIENT, account_hash: bytes, state_root_hash_1: bytes):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_state_get_item.account.json
        assert isinstance(response, dict)
        # TODO: use jsonschema derived from RPC schema
        assert "account_hash" in response
        assert "action_thresholds" in response
        assert "deployment" in response["action_thresholds"]
        assert "key_management" in response["action_thresholds"]
        assert "associated_keys" in response
        assert len(response["associated_keys"]) >= 1
        for key in response["associated_keys"]:
            assert "account_hash" in key
            assert "weight" in key
        assert "main_purse" in response
        assert "named_keys" in response
        assert isinstance(response["named_keys"], list)

    _assert(CLIENT.get_account_info(account_hash, state_root_hash_1))


def test_get_account_main_purse_uref(CLIENT, account_key: bytes, state_root_hash_1: str):
    def _assert(response):
        # e.g. uref-827d5984270fed5aaaf076e1801733414a307ed8c5d85cad8ebe6265ba887b3a-007
        print(response)
        assert isinstance(response, str)
        parts = response.split("-")
        assert len(parts) == 3
        assert parts[0] == "uref"
        assert len(parts[1]) == 64
        assert len(parts[2]) == 3

    _assert(CLIENT.get_account_main_purse_uref(account_key, state_root_hash_1))


def test_get_account_balance(CLIENT, account_main_purse_uref: str, state_root_hash_1: bytes):
    def _assert(response):
        assert isinstance(response, int)
        assert response >= 0

    _assert(CLIENT.get_account_balance(account_main_purse_uref, state_root_hash_1))


def test_get_auction_info(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_state_get_auction_info.json
        assert isinstance(response, dict)

    _assert(CLIENT.get_auction_info())


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
        print(response)
        assert response == sorted(CLIENT.NODE_RPC_ENDPOINTS)

    _assert(CLIENT.get_rpc_endpoint())


def test_get_rpc_endpoint(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, dict)        

    for endpoint in CLIENT.NODE_RPC_ENDPOINTS:
        _assert(CLIENT.get_rpc_endpoint(endpoint))
