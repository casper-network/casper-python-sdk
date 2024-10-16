import argparse
import asyncio
import json
import os
import pathlib
import random
import typing

import pycspr
from pycspr.api import NodeSpeculativeRpcClient as NodeClient
from pycspr.api import NodeSpeculativeRpcConnectionInfo as NodeConnection
from pycspr.type_defs.crypto import KeyAlgorithm
from pycspr.type_defs.crypto import PrivateKey
from pycspr.type_defs.crypto import PublicKey
from pycspr.types.node import Deploy


# Path to CCTL assets.
_PATH_TO_CCTL_ASSETS = pathlib.Path(os.getenv("CCTL")) / "assets"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to invoke a node's speculative JSON-RPC API.")

# CLI argument: path to cp1 secret key - defaults to CCTL user 1.
_ARGS.add_argument(
    "--cp1-secret-key-path",
    default=_PATH_TO_CCTL_ASSETS / "users" / "user-1" / "secret_key.pem",
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

# CLI argument: path to cp2 account key - defaults to CCTL user 2.
_ARGS.add_argument(
    "--cp2-account-key-path",
    default=_PATH_TO_CCTL_ASSETS / "users" / "user-2" / "public_key_hex",
    dest="path_to_cp2_account_key",
    help="Path to counter-party two's public_key_hex file.",
    type=str,
    )

# CLI argument: name of target chain - defaults to CCTL chain.
_ARGS.add_argument(
    "--chain",
    default="cspr-dev-cctl",
    dest="chain_name",
    help="Name of target chain.",
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

# CLI argument: Node API speculative JSON-RPC port - defaults to 25101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc-speculative",
    default=25101,
    dest="node_port_rpc_speculative",
    help="Node API speculative JSON-RPC port.  Typically 7778 on most nodes.",
    type=int,
    )


async def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client: NodeClient = _get_client(args)

    # Set counter-parties.
    cp1, cp2 = _get_counter_parties(args)

    # Set deploy.
    deploy: Deploy = _get_deploy(args, cp1, cp2)

    # Approve deploy.
    deploy.approve(cp1)

    # Dispatch deploy to a node.
    r = await client.speculative_exec(deploy)

    print(json.dumps(r, indent=4))


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr speculative RPC client instance.

    """
    return NodeClient(NodeConnection(args.node_host, args.node_port_rpc_speculative))


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
        target=cp2,
        correlation_id=random.randint(1, int(1e6))
        )

    return deploy


# Entry point.
if __name__ == "__main__":
    asyncio.run(_main(_ARGS.parse_args()))
