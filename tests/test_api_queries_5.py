import pycspr


def test_get_state_item(CLIENT: pycspr.NodeClient, account_hash, state_root_hash):
    def _assert(response):
        assert isinstance(response, dict)

    _assert(CLIENT.get_state_item(
        f"account-hash-{account_hash.hex()}",
        [],
        state_root_hash)
        )
