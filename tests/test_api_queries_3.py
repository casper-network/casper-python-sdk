import pycspr


def test_get_account_balance_under_purse_uref(CLIENT, account_main_purse_uref: object, state_root_hash: bytes):
    assert isinstance(account_main_purse_uref, pycspr.types.CL_URef)

    def _assert(response):
        assert isinstance(response, int)
        assert response >= 0

    _assert(CLIENT.get_account_balance_under_purse_uref(account_main_purse_uref, state_root_hash))


def test_get_account_balance_under_account_key(CLIENT, account_key: bytes, state_root_hash: bytes):
    def _assert(response):
        assert isinstance(response, int)
        assert response >= 0

    _assert(CLIENT.get_account_balance_under_account_key(account_key, state_root_hash))
