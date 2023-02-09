import argparse
import asyncio
import os
import pathlib
import random
import typing

import pycspr
from pycspr import NodeClient
from pycspr import NodeConnection
from pycspr.crypto import KeyAlgorithm
from pycspr.types import PrivateKey
from pycspr.types import Deploy
from pycspr.types import PublicKey


# Path to NCTL assets.
_PATH_TO_NCTL_ASSETS = pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Illustration of how to execute native transfers.")

# CLI argument: path to cp1 secret key - defaults to NCTL user 1.
_ARGS.add_argument(
    "--cp1-secret-key-path",
    default=_PATH_TO_NCTL_ASSETS / "users" / "user-1" / "secret_key.pem",
    dest="path_to_cp1_secret_key",
    help="Path to counter-party one's secret_key.pem file.",
    type=str,
    )

# CLI argument: type of cp1 secret key - defaults to ED25519.
_ARGS.add_argument(
    "--cp1-secret-key-type",
    default=KeyAlgorithm.ED25519.name,
    dest="type_of_cp1_secret_key",
    help="Type of counter party one's secret key.",
    type=str,
    )

# CLI argument: path to cp2 account key - defaults to NCTL user 2.
_ARGS.add_argument(
    "--cp2-account-key-path",
    default=_PATH_TO_NCTL_ASSETS / "users" / "user-2" / "public_key_hex",
    dest="path_to_cp2_account_key",
    help="Path to counter-party two's public_key_hex file.",
    type=str,
    )

# CLI argument: name of target chain - defaults to NCTL chain.
_ARGS.add_argument(
    "--chain",
    default="casper-net-1",
    dest="chain_name",
    help="Name of target chain.",
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

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ NCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc",
    default=11101,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )

# CLI argument: Node API speculative JSON-RPC port - defaults to 25101 @ NCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc-speculative",
    default=25101,
    dest="node_port_rpc_speculative",
    help="Node API speculative JSON-RPC port.  Typically 7778 on most nodes.",
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


async def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client = _get_client(args)

    # Set counter-parties.
    cp1, cp2 = _get_counter_parties(args)

    # Set deploy.
    deploy: Deploy = _get_deploy(args, cp1, cp2)

    # Approve deploy.
    deploy.approve(cp1)

    # Dispatch deploy to a node.
    r = client.speculative_exec(deploy)

    print(r)


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
        port_rpc_speculative=args.node_port_rpc_speculative,
        port_sse=args.node_port_sse
    ))


def _get_counter_parties(args: argparse.Namespace) -> typing.Tuple[PrivateKey, PublicKey]:
    """Returns the 2 counter-parties participating in the transfer.

    """
    cp1 = pycspr.parse_private_key(
        args.path_to_cp1_secret_key,
        args.type_of_cp1_secret_key,
        )
    cp2 = pycspr.parse_public_key(
        args.path_to_cp2_account_key
        )

    return cp1, cp2


def _get_deploy(args: argparse.Namespace, cp1: PrivateKey, cp2: PublicKey) -> Deploy:
    """Returns transfer deploy to be dispatched to a node.

    """
    # Set standard deploy parameters.
    deploy_params = pycspr.create_deploy_parameters(
        account=cp1,
        chain_name=args.chain_name
        )

    # Set deploy.
    deploy = pycspr.create_transfer(
        params=deploy_params,
        amount=int(2.5e9),
        target=cp2.account_key,
        correlation_id=random.randint(1, 1e6)
        )

    return deploy


# Entry point.
if __name__ == "__main__":
    asyncio.run(_main(_ARGS.parse_args()))
