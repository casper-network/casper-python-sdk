from pycspr import NodeRpcClient
from pycspr.types.node import StateRootHash
from pycspr.types.node import Address


async def test_get_state_item(
    SIDECAR_RPC_CLIENT: NodeRpcClient,
    account_hash: Address,
    state_root_hash: StateRootHash
):
    account_hash = f"account-hash-{account_hash.hex()}"
    data = await SIDECAR_RPC_CLIENT.get_state_item(account_hash, [], state_root_hash)

    assert isinstance(data, dict)
    assert "Account" in data
