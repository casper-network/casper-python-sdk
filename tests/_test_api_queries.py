def test_get_state_root_hash(LIB):
    def _assert(response):
        # e.g. 6e1f211643d870e1f3135ed85d64ba1ee212304d889692d16d0291d3bbdf1712
        assert isinstance(response, str)
        assert len(response) == 64

    for block_id in (None, 1):
        _assert(LIB.get_state_root_hash(block_id))


def test_get_account_info(LIB, account_key, state_root_hash):
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

    _assert(LIB.get_account_info(account_key, state_root_hash))


def test_get_account_main_purse_uref(LIB, account_key, state_root_hash):
    def _assert(response):
        # e.g. uref-827d5984270fed5aaaf076e1801733414a307ed8c5d85cad8ebe6265ba887b3a-007
        assert isinstance(response, str)
        parts = response.split("-")
        assert len(parts) == 3
        assert parts[0] == "uref"
        assert len(parts[1]) == 64
        assert len(parts[2]) == 3

    _assert(LIB.get_account_main_purse_uref(account_key, state_root_hash))


def test_get_account_balance_01(LIB, account_main_purse_uref, state_root_hash):
    def _assert(response):
        # e.g. 1000000000000000000000000000000000
        assert isinstance(response, int)
        assert response >= 0

    _assert(LIB.get_account_balance(account_main_purse_uref, state_root_hash))


def test_get_account_balance_02(LIB, account_main_purse_uref, state_root_hash):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_state_get_balance.json
        assert isinstance(response, dict)

    _assert(LIB.get_account_balance(account_main_purse_uref, state_root_hash, parse_response=False))


def test_get_auction_info(LIB):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_state_get_auction_info.json
        assert isinstance(response, dict)

    _assert(LIB.get_auction_info())


def test_get_node_metrics_01(LIB):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_metrics.json
        assert isinstance(response, list)
        assert len(response) > 300

    _assert(LIB.get_node_metrics())


def test_get_node_metrics_02(LIB):
    def _assert(response):
        # e.g. docs/api_reponses/rest_metrics.json
        assert isinstance(response, list)
        assert len(response) == 1

    _assert(LIB.get_node_metrics("mem_deploy_gossiper"))


def test_get_node_peers(LIB):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_info_get_peers.json
        assert isinstance(response, list)

    _assert(LIB.get_node_peers())


def test_get_node_status(LIB):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_info_get_status.json
        assert isinstance(response, dict)

    _assert(LIB.get_node_status())


def test_get_block_01(LIB):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_chain_get_block.json
        assert isinstance(response, dict)
        assert "body" in response        
        assert "hash" in response        
        assert "header" in response        
        assert "proofs" in response        

    for block_id in (None, 1):
        _assert(LIB.get_block(block_id))


def test_get_block_02(LIB, block_hash):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_chain_get_block.json
        assert isinstance(response, dict)
        assert "body" in response        
        assert "hash" in response        
        assert "header" in response        
        assert "proofs" in response        

    _assert(LIB.get_block(block_hash))


def test_get_switch_block(LIB):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_chain_get_block.json
        assert response["header"]["era_end"] is not None

    _assert(LIB.get_switch_block())


def test_get_era_info(LIB, switch_block_hash):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_chain_get_era_info_by_switch_block.json
        assert isinstance(response, dict)
        assert "block_hash" in response
        assert "era_id" in response
        assert "merkle_proof" in response
        assert "state_root_hash" in response
        assert "stored_value" in response
        assert "EraInfo" in response["stored_value"]
        assert "seigniorage_allocations" in response["stored_value"]["EraInfo"]

    _assert(LIB.get_era_info(switch_block_hash))


def test_get_rpc_schema(LIB):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, dict)
        assert "openrpc" in response

    _assert(LIB.get_rpc_schema())


def test_get_rpc_endpoint_01(LIB):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, list)
        assert response == sorted(LIB.NODE_RPC_ENDPOINTS)

    _assert(LIB.get_rpc_endpoint())


def test_get_rpc_endpoint_02(LIB):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, dict)        

    for endpoint in LIB.NODE_RPC_ENDPOINTS:
        _assert(LIB.get_rpc_endpoint(endpoint))
