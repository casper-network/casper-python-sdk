import argparse
import os
import pathlib
import random
import typing

import pycspr
from pycspr.client import NodeClient
from pycspr.client import NodeConnectionInfo
from pycspr.types import Deploy
from pycspr.types import PrivateKey
from pycspr.types import PublicKey
from pycspr.types import UnforgeableReference



# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to execute native transfers with pycspr.")

# CLI argument: path to cp2 account key - defaults to NCTL user 2.
_ARGS.add_argument(
    "--account-key-path",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "users" / "user-1" / "public_key_hex",
    dest="path_to_account_key",
    help="Path to a test user's public_key_hex file.",
    type=str,
    )

# CLI argument: host address of target node - defaults to NCTL node 1.
_ARGS.add_argument(
    "--node-host",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API REST port - defaults to 14101 @ NCTL node 1.
_ARGS.add_argument(
    "--node-port-rest",
    default=14101,
    dest="node_port_rest",
    help="Node API REST port.  Typically 8888 on most nodes.",
    type=int,
    )

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ NCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc",
    default=11101,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )

# CLI argument: Node API SSE port - defaults to 18101 @ NCTL node 1.
_ARGS.add_argument(
    "--node-port-sse",
    default=18101,
    dest="node_port_sse",
    help="Node API SSE port.  Typically 9999 on most nodes.",
    type=int,
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set client.
    client = _get_client(args)

    # Set account key of test user.
    user_public_key = pycspr.factory.parse_public_key(args.path_to_account_key)      

    # Query 0.1: get_rpc_schema.
    rpc_schema: typing.List[dict] = client.queries.get_rpc_schema()
    assert isinstance(rpc_schema, dict)
    print("SUCCESS :: Query 0.1: get_rpc_schema")

    # Query 0.2: get_rpc_endpoints.
    rpc_endpoints: typing.List[str] = client.queries.get_rpc_endpoints()
    assert isinstance(rpc_endpoints, list)
    print("SUCCESS :: Query 0.2: get_rpc_endpoints")

    # Query 0.3: get_rpc_endpoint.
    rpc_endpoint: dict = client.queries.get_rpc_endpoint("account_put_deploy")
    assert isinstance(rpc_endpoint, dict)
    print("SUCCESS :: Query 0.3: get_rpc_endpoint")

    # Query 1.1: get_node_metrics.
    node_metrics: typing.List[str] = client.queries.get_node_metrics()
    assert isinstance(node_metrics, list)
    print("SUCCESS :: Query 1.1: get_node_metrics")

    # Query 1.2: get_node_metric.
    node_metric: typing.List[str] = client.queries.get_node_metric("mem_deploy_gossiper")
    assert isinstance(node_metrics, list)
    print("SUCCESS :: Query 1.2: get_node_metric")

    # Query 1.3: get_node_peers.
    node_peers: typing.List[dict] = client.queries.get_node_peers()
    assert isinstance(node_peers, list)
    print("SUCCESS :: Query 1.3: get_node_peers")

    # Query 1.4: get_node_status.
    node_status: typing.List[dict] = client.queries.get_node_status()
    assert isinstance(node_status, dict)
    print("SUCCESS :: Query 1.4: get_node_status")

    # Query 2.1: get_state_root_hash - required for global state related queries.
    state_root_hash: bytes = client.queries.get_state_root_hash()
    assert isinstance(state_root_hash, bytes)
    print("SUCCESS :: Query 2.1: get_state_root_hash")

    # Query 2.2: get_account_info.
    account_info = client.queries.get_account_info(user_public_key.account_key)
    assert isinstance(account_info, dict)
    print("SUCCESS :: Query 2.2: get_account_info")

    # Query 2.3: get_account_main_purse_uref.
    account_main_purse = client.queries.get_account_main_purse_uref(user_public_key.account_key)
    assert isinstance(account_main_purse, UnforgeableReference)
    print("SUCCESS :: Query 2.3: get_account_main_purse_uref")

    # Query 2.4: get_account_balance.
    account_balance = client.queries.get_account_balance(account_main_purse, state_root_hash)
    assert isinstance(account_balance, int)
    print("SUCCESS :: Query 2.4: get_account_balance")

    # Query 3.1: get_block_at_era_switch - will poll until switch block.
    print("POLLING :: Query 3.1: get_block_at_era_switch - may take some time")
    block: dict = client.queries.get_block_at_era_switch()
    assert isinstance(block, dict)
    print("SUCCESS :: Query 3.1: get_block_at_era_switch")

    # Query 3.2: get_block - by hash & by height.    
    assert client.queries.get_block(block["hash"]) == \
           client.queries.get_block(block["header"]["height"])
    print("SUCCESS :: Query 3.2: get_block - by hash & by height")

    # Query 3.3: get_block_transfers - by hash & by height.
    block_transfers = client.queries.get_block_transfers(block["hash"])
    assert isinstance(block_transfers, tuple)
    assert isinstance(block_transfers[0], str)      # black hash
    assert isinstance(block_transfers[1], list)     # set of transfers
    assert block_transfers == client.queries.get_block_transfers(block["header"]["height"])
    print("SUCCESS :: Query 3.3: get_block_transfers - by hash & by height")

    # Query 4.1: get_auction_info.
    auction_info = client.queries.get_auction_info()
    assert isinstance(auction_info, dict)
    print("SUCCESS :: Query 4.1: get_auction_info")

    # Query 4.2: get_era_info - by switch block hash.
    era_info = client.queries.get_era_info(block["hash"])
    assert isinstance(era_info, dict)
    print("SUCCESS :: Query 4.2: get_era_info - by switch block hash")

    # Query 4.3: get_era_info - by switch block height.
    assert client.queries.get_era_info(block["hash"]) == \
           client.queries.get_era_info(block["header"]["height"])
    print("SUCCESS :: Query 4.3: get_era_info - by switch block height")



def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    connection = NodeConnectionInfo(
        host=args.node_host,
        port_rest=args.node_port_rest,
        port_rpc=args.node_port_rpc,
        port_sse=args.node_port_sse
    )

    return NodeClient(connection)


def _get_counter_parties(args: argparse.Namespace) -> PublicKey:
    """Returns the 2 counter-parties participating in the transfer.

    """

    return pycspr.factory.parse_public_key(
        args.path_to_cp2_account_key
        )    

    return cp1, cp2


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
