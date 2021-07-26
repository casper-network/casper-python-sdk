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
_ARGS = argparse.ArgumentParser("Demo illustrating how to undelegate CSPR tokens from a validator.")

# CLI argument: path to delegator secret key - defaults to NCTL user 1.
_ARGS.add_argument(
    "--delegator-secret-key-path",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "users" / "user-1" / "secret_key.pem",
    dest="path_to_delegator_secret_key",
    help="Path to delegator's secret_key.pem file.",
    type=str,
    )

# CLI argument: type of delegator secret key - defaults to ED25519.
_ARGS.add_argument(
    "--delegator-secret-key-type",
    default=pycspr.KeyAlgorithm.ED25519.name,
    dest="type_of_delegator_secret_key",
    help="Type of delegator's secret key.",
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

# CLI argument: path to session code wasm binary - defaults to NCTL bin/eco/undelegate.wasm.
_ARGS.add_argument(
    "--path-to-wasm",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "bin" / "auction" / "undelegate.wasm",
    dest="path_to_wasm",
    help="Path to delegate.wasm file.",
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


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set counter-parties.
    delegator, validator = _get_counter_parties(args)

    # Set deploy.
    deploy = _get_deploy(args, delegator, validator)

    # Approve deploy.
    deploy.set_approval(pycspr.create_deploy_approval(deploy, delegator))    

    # Dispatch deploy to a node.
    client = _get_client(args)
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


def _get_counter_parties(args: argparse.Namespace) -> typing.Tuple[PrivateKey, PublicKey]:
    """Returns the 2 counter-parties participating in the delegation.

    """
    delegator = pycspr.parse_private_key(
        args.path_to_delegator_secret_key,
        args.type_of_delegator_secret_key,
        )
    validator = pycspr.parse_public_key(
        args.path_to_validator_account_key
        )    

    return delegator, validator


def _get_deploy(args: argparse.Namespace, delegator: PrivateKey, validator: PublicKey) -> Deploy:
    """Returns delegation deploy to be dispatched to a node.

    """
    # Set standard deploy parameters.
    deploy_params = pycspr.create_deploy_parameters(
        account=delegator,
        chain_name=args.chain_name
        )

    # Set deploy.
    deploy = pycspr.create_standard_delegation_withdrawal(
        params=deploy_params,
        amount=int(1e9),
        public_key_of_delegator=delegator,
        public_key_of_validator=validator,
        path_to_contract=args.path_to_wasm
        )

    return deploy


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
