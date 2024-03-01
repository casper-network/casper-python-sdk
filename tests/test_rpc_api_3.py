from pycspr import NodeRpcClient


def test_get_state_item(RPC_CLIENT: NodeRpcClient, account_hash: bytes, state_root_hash: str):
    account_hash = f"account-hash-{account_hash.hex()}"
    data = RPC_CLIENT.get_state_item(account_hash, [], state_root_hash)

    assert isinstance(data, dict)
    assert "Account" in data
