import argparse
import os
import pathlib
import random
import typing

import pycspr
from pycspr.client import NodeClient
from pycspr.client import NodeConnectionInfo
from pycspr.crypto import KeyAlgorithm
from pycspr.types import Deploy
from pycspr.types import PrivateKey
from pycspr.types import PublicKey
from pycspr.types import UnforgeableReference



# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to unstake CSPR tokens as a validator.")

# CLI argument: path to validator secret key - defaults to NCTL user 1.
_ARGS.add_argument(
    "--validator-secret-key-path",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "nodes" / "node-1" / "keys" / "secret_key.pem",
    dest="path_to_validator_secret_key",
    help="Path to validator's secret_key.pem file.",
    type=str,
    )

# CLI argument: type of validator secret key - defaults to ED25519.
_ARGS.add_argument(
    "--validator-secret-key-type",
    default=KeyAlgorithm.ED25519.name,
    dest="type_of_validator_secret_key",
    help="Type of validator's secret key.",
    type=str,
    )

# CLI argument: path to session code wasm binary - defaults to NCTL bin/eco/withdraw_bid.wasm.
_ARGS.add_argument(
    "--path-to-wasm",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "bin" / "auction" / "withdraw_bid.wasm",
    dest="path_to_wasm",
    help="Path to withdraw_bid.wasm file.",
    type=str,
    )

# CLI argument: amount to unstake, i.e. unbond, from the network.
_ARGS.add_argument(
    "--amount",
    default=1000000000000001,
    dest="amount",
    help="Amount to unbond.",
    type=int,
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


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client = _get_client(args)

    # Set validator key.
    validator: PrivateKey = pycspr.factory.create_private_key(
        args.path_to_validator_secret_key,
        args.type_of_validator_secret_key,
        )
    
    # Set validator unbond purse.
    validator_purse: UnforgeableReference = \
        client.queries.get_account_main_purse_uref(validator.account_key)

    # Set deploy.
    deploy: Deploy = _get_deploy(args, validator, validator_purse)

    # Approve deploy.
    deploy.approve(validator)

    # Dispatch deploy.
    client.deploys.send(deploy)

    print(f"Deploy dispatched to node [{args.node_host}]: {deploy.hash.hex()}")


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    connection = NodeConnectionInfo(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    )

    return NodeClient(connection)


def _get_deploy(
    args: argparse.Namespace,
    validator: PrivateKey,
    validator_purse: UnforgeableReference
    ) -> Deploy:
    """Returns delegation deploy to be dispatched to a node.

    """
    # Set standard deploy parameters.
    deploy_params = pycspr.factory.create_deploy_parameters(
        account=validator,
        chain_name=args.chain_name
        )

    # Set deploy.
    deploy = pycspr.factory.create_validator_auction_bid_withdrawal(
        params=deploy_params,
        amount=args.amount,
        public_key=validator.as_public_key(),
        path_to_wasm=args.path_to_wasm,
        unbond_purse=validator_purse,
        )

    return deploy


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())

