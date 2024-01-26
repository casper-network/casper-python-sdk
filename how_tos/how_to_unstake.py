import argparse
import os
import pathlib

import pycspr
from pycspr import NodeClient
from pycspr import NodeConnection
from pycspr.crypto import KeyAlgorithm
from pycspr.types import Deploy
from pycspr.types import PrivateKey
from pycspr.types import CL_URef


# Path to CCTL assets.
_PATH_TO_CCTL_ASSETS = pathlib.Path(os.getenv("CCTL")) / "assets"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to unstake CSPR tokens as a validator.")

# CLI argument: path to validator secret key - defaults to CCTL user 1.
_ARGS.add_argument(
    "--validator-secret-key-path",
    default=_PATH_TO_CCTL_ASSETS / "nodes" / "node-1" / "keys" / "secret_key.pem",
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

# CLI argument: path to session code wasm binary - defaults to CCTL bin/wasm/withdraw_bid.wasm.
_ARGS.add_argument(
    "--path-to-wasm",
    default=_PATH_TO_CCTL_ASSETS / "bin" / "wasm" / "withdraw_bid.wasm",
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

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ CCTL node 1.
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
    validator: PrivateKey = pycspr.parse_private_key(
        args.path_to_validator_secret_key,
        args.type_of_validator_secret_key,
        )

    # Set validator unbond purse.
    validator_purse_uref: CL_URef = \
        client.get_account_main_purse_uref(validator.account_key)

    # Set deploy.
    deploy: Deploy = _get_deploy(args, validator, validator_purse_uref)

    # Approve deploy.
    deploy.approve(validator)

    # Dispatch deploy.
    client.send_deploy(deploy)

    print(f"Deploy dispatched to node [{args.node_host}]: {deploy.hash.hex()}")


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    ))


def _get_deploy(
    args: argparse.Namespace,
    validator: PrivateKey,
    validator_purse_uref: CL_URef
) -> Deploy:
    """Returns delegation deploy to be dispatched to a node.

    """
    # Set standard deploy parameters.
    deploy_params = pycspr.create_deploy_parameters(
        account=validator,
        chain_name=args.chain_name
        )

    # Set deploy.
    deploy = pycspr.create_validator_auction_bid_withdrawal(
        params=deploy_params,
        amount=args.amount,
        public_key=validator.as_public_key,
        path_to_wasm=args.path_to_wasm,
        unbond_purse_ref=validator_purse_uref,
        )

    return deploy


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
