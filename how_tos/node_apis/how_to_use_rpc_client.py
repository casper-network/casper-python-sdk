import argparse
import os
import pathlib
import typing

import pycspr
from pycspr import NodeRpcClient as NodeClient
from pycspr import NodeConnectionInfo
from pycspr.api.rpc import types as types
from pycspr.api.rpc import types as rpc_types
from pycspr.api.rpc.codec import decode as decoder
from pycspr.types import CL_URef
from pycspr.types import GlobalStateID
from pycspr.types import GlobalStateIDType
from pycspr.types import PurseID
from pycspr.types import PurseIDType


# Path to CCTL assets.
_PATH_TO_CCTL_ASSETS = pathlib.Path(os.getenv("CCTL")) / "assets"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to execute native transfers with pycspr.")

# CLI argument: path to cp2 account key - defaults to CCTL user 2.
_ARGS.add_argument(
    "--account-key-path",
    default=_PATH_TO_CCTL_ASSETS / "users" / "user-1" / "public_key_hex",
    dest="path_to_account_key",
    help="Path to a test user's public_key_hex file.",
    type=str,
    )

# CLI argument: host address of target node - defaults to CCTL node 1.
_ARGS.add_argument(
    "--node-host",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API REST port - defaults to 14101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rest",
    default=14101,
    dest="node_port_rest",
    help="Node API REST port.  Typically 8888 on most nodes.",
    type=int,
    )

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc",
    default=11101,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )

# CLI argument: Node API SSE port - defaults to 18101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-sse",
    default=18101,
    dest="node_port_sse",
    help="Node API SSE port.  Typically 9999 on most nodes.",
    type=int,
    )


class _Context():
    def __init__(self, args: argparse.Namespace):
        self.client = NodeClient(NodeConnectionInfo(
            host=args.node_host,
            port_rest=args.node_port_rest,
            port_rpc=args.node_port_rpc,
        ))
        self.user_public_key = pycspr.parse_public_key(args.path_to_account_key)


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Use Node RPC Client")
    print("-" * 74)

    ctx = _Context(args)
    for func in [
        _get_node_rpc,
        _get_node_ops,
        _get_chain_block,
        _get_chain_block_at_era_switch,
        _get_chain_block_transfers,
        _get_chain_era_info,
        _get_chain_era_summary,
        _get_chain_auction_state,
        _get_chain_validator_changes,
        _get_chain_specification,
        _get_chain_state_root_hash,
        _get_chain_account_info,
    ]:
        func(ctx)
        print("-" * 74)


def _get_chain_account_info(ctx: _Context):
    state_root_hash: bytes = ctx.client.get_state_root()

    # Query: get_account_info.
    account_info: dict = ctx.client.get_account_info(ctx.user_public_key.account_key)
    assert isinstance(account_info, dict)
    print("SUCCESS :: get_account_info")

    # Query: get_account_main_purse_uref.
    account_main_purse: CL_URef = \
        ctx.client.get_account_main_purse_uref(ctx.user_public_key.account_key)
    assert isinstance(account_main_purse, CL_URef)
    print("SUCCESS :: get_account_main_purse_uref")

    # Query: get_account_balance.
    global_state_id = GlobalStateID(state_root_hash, GlobalStateIDType.STATE_ROOT_HASH)
    purse_id = PurseID(account_main_purse, PurseIDType.UREF)
    account_balance: int = ctx.client.get_account_balance(purse_id, global_state_id)
    assert isinstance(account_balance, int)
    print("SUCCESS :: get_account_balance")


def _get_chain_auction_state(ctx: _Context):
    block: dict = ctx.client.get_block()

    for block_id in {
        None,
        block["hash"],
        block["header"]["height"]
    }:
        # Invoke API.
        obj: rpc_types.AuctionState = ctx.client.get_auction_state(block_id)
        assert isinstance(obj, rpc_types.AuctionState)
        print(f"SUCCESS :: get_auction_state :: block-id={block_id}")

    assert ctx.client.get_auction_state(block["hash"]) == \
           ctx.client.get_auction_state(block["header"]["height"])
    print("SUCCESS :: get_auction_state - by equivalent block height & hash")


def _get_chain_block(ctx: _Context):
    # Query: get_block.
    block: dict = ctx.client.get_block()
    assert isinstance(block, dict)
    print("SUCCESS :: get_block :: block-id=None")

    for block_id in {
        block["hash"],
        block["header"]["height"]
    }:
        block: bytes = ctx.client.get_block(block_id)
        assert isinstance(block, dict)
        print(f"SUCCESS :: get_block :: block-id={block_id}")

    assert ctx.client.get_block(block["hash"]) == \
           ctx.client.get_block(block["header"]["height"])
    print("SUCCESS :: get_block - by equivalent height & hash")


def _get_chain_block_at_era_switch(ctx: _Context):
    # Query: get_block_at_era_switch - polls until switch block.
    print("POLLING :: get_block_at_era_switch - may take some time")
    block: dict = ctx.client.get_block_at_era_switch()
    assert isinstance(block, dict)
    print("SUCCESS :: get_block_at_era_switch")


def _get_chain_block_transfers(ctx: _Context):
    block: dict = ctx.client.get_block()

    # Query: by hash.
    entity: rpc_types.BlockTransfers = ctx.client.get_block_transfers(block["hash"])
    assert isinstance(entity, rpc_types.BlockTransfers)
    print("SUCCESS :: invoked get_block_transfers - by block hash")

    # Query: by height.
    assert entity == ctx.client.get_block_transfers(block["header"]["height"])
    print("SUCCESS :: invoked get_block_transfers - by block height")


def _get_chain_era_info(ctx: _Context):
    print("POLLING :: get_block_at_era_switch - may take some time")
    block: dict = ctx.client.get_block_at_era_switch()

    for block_id in {
        None,
        block["hash"],
        block["header"]["height"]
    }:
        era_info: dict = ctx.client.get_era_info(block_id)
        assert isinstance(era_info, dict)
        print(f"SUCCESS :: get_era_info :: block-id={block_id}")
        assert era_info == ctx.client.get_era_info_by_switch_block(block_id)

    assert ctx.client.get_era_info(block["hash"]) == \
           ctx.client.get_era_info(block["header"]["height"])
    print("SUCCESS :: get_era_info - by equivalent block height & hash")


def _get_chain_era_summary(ctx: _Context):
    block: dict = ctx.client.get_block()

    for block_id in {
        None,
        block["hash"],
        block["header"]["height"]
    }:
        entity: types.EraSummary = ctx.client.get_era_summary(block_id)
        assert isinstance(entity, types.EraSummary)
        print(f"SUCCESS :: get_era_summary :: block-id={block_id}")

    assert ctx.client.get_era_summary(block["hash"]) == \
           ctx.client.get_era_summary(block["header"]["height"])
    print("SUCCESS :: get_era_summary :: by equivalent block height & hash")


def _get_chain_specification(ctx: _Context):
    chainspec: dict = ctx.client.get_chainspec()
    assert isinstance(chainspec, dict)


def _get_chain_state_root_hash(ctx: _Context):
    block: dict = ctx.client.get_block()

    for block_id in {
        None,
        block["hash"],
        block["header"]["height"]
    }:
        state_root_hash: bytes = ctx.client.get_state_root(block_id)
        assert isinstance(state_root_hash, bytes)
        print(f"SUCCESS :: get_state_root_hash :: block-id={block_id}")

    assert ctx.client.get_state_root(block["hash"]) == \
           ctx.client.get_state_root(block["header"]["height"])
    print("SUCCESS :: get_state_root_hash :: by equivalent switch block height & hash")


def _get_chain_validator_changes(ctx: _Context):
    validator_changes: typing.List[rpc_types.ValidatorChanges] = ctx.client.get_validator_changes()
    assert isinstance(validator_changes, list)
    for item in validator_changes:
        assert isinstance(item, types.ValidatorChanges)
    print("SUCCESS :: get_validator_changes")


def _get_node_ops(ctx: _Context):
    # get_node_metrics.
    node_metrics: typing.List[str] = ctx.client.get_node_metrics()
    assert isinstance(node_metrics, list)
    print("SUCCESS :: get_node_metrics")

    # get_node_metric.
    node_metric: typing.List[str] = ctx.client.get_node_metric("mem_deploy_gossiper")
    assert isinstance(node_metric, list)
    print("SUCCESS :: get_node_metric")

    # get_node_peers.
    node_peers: typing.List[dict] = ctx.client.get_node_peers()
    assert isinstance(node_peers, list)
    print("SUCCESS :: get_node_peers")

    # get_node_status.
    node_status: dict = ctx.client.get_node_status()
    assert isinstance(node_status, dict)
    print("SUCCESS :: get_node_status")


def _get_node_rpc(ctx: _Context):
    # get_rpc_schema.
    rpc_schema: dict = ctx.client.get_rpc_schema()
    assert isinstance(rpc_schema, dict)
    print("SUCCESS :: get_rpc_schema")

    # get_rpc_endpoints.
    rpc_endpoints: typing.List[str] = ctx.client.get_rpc_endpoints()
    assert isinstance(rpc_endpoints, list)
    print("SUCCESS :: get_rpc_endpoints")

    # get_rpc_endpoint.
    for rpc_endpoint in rpc_endpoints:
        rpc_endpoint_schema: dict = ctx.client.get_rpc_endpoint("account_put_deploy")
        assert isinstance(rpc_endpoint_schema, dict)
    print("SUCCESS :: get_rpc_endpoint")


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
