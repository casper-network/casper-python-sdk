import pycspr
from pycspr.api.rpc import types as rpc_types


def test_get_auction_info(RPC_CLIENT: pycspr.NodeRpcClient):
    data = RPC_CLIENT.get_auction_info()
    assert isinstance(data, rpc_types.AuctionState)

    data = RPC_CLIENT.get_auction_info(decode=False)
    assert isinstance(data, dict)


def test_get_era_info_by_switch_block(RPC_CLIENT: pycspr.NodeRpcClient, switch_block_hash: str):
    data = RPC_CLIENT.get_era_info_by_switch_block(switch_block_hash)
    assert isinstance(data, dict)


def test_get_era_summary(RPC_CLIENT: pycspr.NodeRpcClient, block_hash: str):
    data = RPC_CLIENT.get_era_summary(block_hash)
    assert isinstance(data, rpc_types.EraSummary)

    data = RPC_CLIENT.get_era_summary(block_hash, decode=False)
    assert isinstance(data, dict)
