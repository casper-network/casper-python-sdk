import pycspr


def test_get_account_balance_under_purse_uref(CLIENT, account_main_purse_uref: object, state_root_hash: bytes):
    assert isinstance(account_main_purse_uref, pycspr.types.CL_URef)

    def _assert(response):
        assert isinstance(response, int)
        assert response >= 0

    _assert(CLIENT.get_account_balance(account_main_purse_uref, state_root_hash))


def test_get_account_balance_under_account_hash(CLIENT, account_hash: bytes, state_root_hash: bytes):
    def _assert(response):
        assert isinstance(response, int)
        assert response >= 0

    _assert(CLIENT.get_account_balance(account_hash, state_root_hash))


def test_get_account_balance_under_account_key(CLIENT, account_key: bytes, state_root_hash: bytes):
    def _assert(response):
        assert isinstance(response, int)
        assert response >= 0

    _assert(CLIENT.get_account_balance(account_key, state_root_hash))
