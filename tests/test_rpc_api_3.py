import pycspr


def test_get_state_item(CLIENT: pycspr.NodeClient, account_hash: bytes, state_root_hash: str):
    account_hash = f"account-hash-{account_hash.hex()}"
    data = CLIENT.get_state_item(account_hash, [], state_root_hash)

    assert isinstance(data, dict)
    assert "Account" in data
