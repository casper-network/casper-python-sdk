from pycspr import NodeRpcClient
from pycspr.types.api.rpc import AuctionState
from pycspr.types.api.rpc import EraSummary


def test_get_auction_info(RPC_CLIENT: NodeRpcClient):
    data = RPC_CLIENT.get_auction_info()
    assert isinstance(data, AuctionState)

    data = RPC_CLIENT.get_auction_info(decode=False)
    assert isinstance(data, dict)


def test_get_era_info_by_switch_block(RPC_CLIENT: NodeRpcClient, switch_block_hash: str):
    data = RPC_CLIENT.get_era_info_by_switch_block(switch_block_hash)
    assert isinstance(data, dict)


def test_get_era_summary(RPC_CLIENT: NodeRpcClient, block_hash: str):
    data = RPC_CLIENT.get_era_summary(block_hash)
    assert isinstance(data, EraSummary)

    data = RPC_CLIENT.get_era_summary(block_hash, decode=False)
    assert isinstance(data, dict)
