import pycspr



def test_get_state_root_hash(CLIENT):
    def _assert(response):
        assert isinstance(response, bytes)
        assert len(response) == 32

    for block_id in (None, 1):
        _assert(CLIENT.get_state_root_hash(block_id))


def test_get_account_info(CLIENT, account_key: bytes):
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

    _assert(CLIENT.get_account_info(account_key))


def test_get_account_main_purse_uref(CLIENT, account_key: bytes):
    def _assert(response):
        # e.g. uref-827d5984270fed5aaaf076e1801733414a307ed8c5d85cad8ebe6265ba887b3a-007
        assert isinstance(response, pycspr.types.UnforgeableReference)
        assert len(response.address) == 32
        assert response.access_rights == pycspr.types.CLAccessRights.READ_ADD_WRITE

    _assert(CLIENT.get_account_main_purse_uref(account_key))


def test_get_account_balance(CLIENT, account_main_purse_uref: object, state_root_hash: bytes):
    assert isinstance(account_main_purse_uref, pycspr.types.UnforgeableReference)

    def _assert(response):
        assert isinstance(response, int)
        assert response >= 0

    _assert(CLIENT.get_account_balance(account_main_purse_uref, state_root_hash))
