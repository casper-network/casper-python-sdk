import argparse
import os
import pathlib
import random
import typing

import pycspr
from pycspr.types import PrivateKey
from pycspr.types import Deploy
from pycspr.types import PublicKey



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
    default=pycspr.KeyAlgorithm.ED25519.name,
    dest="type_of_validator_secret_key",
    help="Type of validator's secret key.",
    type=str,
    )

# CLI argument: path to validator's account key - defaults to NCTL node 1.
_ARGS.add_argument(
    "--validator-account-key-path",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "nodes" / "node-1" / "keys" / "public_key_hex",
    dest="path_to_validator_account_key",
    help="Path to validator's public_key_hex file.",
    type=str,
    )

# CLI argument: path to session code wasm binary - defaults to NCTL bin/eco/add_bid.wasm.
_ARGS.add_argument(
    "--path-to-wasm",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "bin" / "auction" / "add_bid.wasm",
    dest="path_to_wasm",
    help="Path to add_bid.wasm file.",
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


# Default withdrawal amount.
_WITHDRAWAL_AMOUNT = 1000000000000001



def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client = _get_client(args)

    # Set validator key.
    validator = pycspr.parse_private_key(
        args.path_to_validator_secret_key,
        args.type_of_validator_secret_key,
        )
    
    # Set validator unbond purse.
    unbond_purse = client.queries.get_account_main_purse_uref(validator.account_key)

    # Set deploy.
    deploy = _get_deploy(args, validator, unbond_purse)

    # Approve deploy.
    deploy.approve(validator)

    # Dispatch deploy.
    client.deploys.send(deploy)

    print(f"Deploy dispatched to node [{args.node_host}]: {deploy.hash.hex()}")


def _get_client(args: argparse.Namespace) -> pycspr.NodeClient:
    """Returns a pycspr client instance.

    """
    connection = pycspr.NodeConnectionInfo(
        host=args.node_host,
        port_rest=args.node_port_rest,
        port_rpc=args.node_port_rpc,
        port_sse=args.node_port_sse
    )

    return pycspr.NodeClient(connection)


def _get_deploy(args: argparse.Namespace, validator: PrivateKey, unbond_purse: str) -> Deploy:
    """Returns delegation deploy to be dispatched to a node.

    """
    # Set standard deploy parameters.
    deploy_params = pycspr.create_deploy_parameters(
        account=validator,
        chain_name=args.chain_name
        )

    # Set deploy.
    deploy = pycspr.create_standard_bid_withdrawal(
        params=deploy_params,
        amount=_WITHDRAWAL_AMOUNT,
        public_key=validator.as_public_key(),
        path_to_contract=args.path_to_wasm,
        unbond_purse=unbond_purse,
        )

    return deploy


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
