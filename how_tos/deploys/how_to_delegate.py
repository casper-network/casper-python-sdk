import argparse
import asyncio
import os
import pathlib
import typing

import pycspr
from pycspr import NodeRpcClient as NodeClient
from pycspr import NodeRpcConnectionInfo as NodeConnectionInfo
from pycspr.type_defs.crypto import KeyAlgorithm
from pycspr.type_defs.crypto import PrivateKey
from pycspr.type_defs.crypto import PublicKey
from pycspr.types.node import Deploy


# Path to CCTL assets.
_PATH_TO_CCTL_ASSETS = pathlib.Path(os.getenv("CCTL")) / "assets"
_PATH_TO_CCTL_NODE = _PATH_TO_CCTL_ASSETS / "nodes" / "node-1"
_PATH_TO_CCTL_USER = _PATH_TO_CCTL_ASSETS / "users" / "user-1"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("How to delegate CSPR to a validator.")

# CLI argument: path to delegator secret key - defaults to CCTL user 1.
_ARGS.add_argument(
    "--delegator-secret-key-path",
    default=_PATH_TO_CCTL_USER / "secret_key.pem",
    dest="path_to_delegator_secret_key",
    help="Path to delegator's secret_key.pem file.",
    type=str,
    )

# CLI argument: type of delegator secret key - defaults to ED25519.
_ARGS.add_argument(
    "--delegator-secret-key-type",
    default=KeyAlgorithm.ED25519.name,
    dest="type_of_delegator_secret_key",
    help="Type of delegator's secret key.",
    type=str,
    )

# CLI argument: path to validator's account key - defaults to CCTL node 1.
_ARGS.add_argument(
    "--validator-account-key-path",
    default=_PATH_TO_CCTL_NODE / "keys" / "public_key_hex",
    dest="path_to_validator_account_key",
    help="Path to validator's public_key_hex file.",
    type=str,
    )

# CLI argument: path to session code wasm binary.
_ARGS.add_argument(
    "--path-to-wasm",
    default=_PATH_TO_CCTL_ASSETS / "bin" / "delegate.wasm",
    dest="path_to_wasm",
    help="Path to delegate.wasm file.",
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

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc",
    default=11101,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )


async def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Delegate")
    print("")
    print("Illustrates usage of pycspr.create_validator_delegation function.")
    print("-" * 74)

    # Set node client.
    client: NodeClient = _get_client(args)

    # Set counter-parties.
    delegator, validator = _get_counter_parties(args)

    # Set deploy.
    deploy: Deploy = _get_deploy(args, delegator, validator)

    # Approve deploy.
    deploy.approve(delegator)

    # Dispatch deploy to a node.
    await client.send_deploy(deploy)

    print(f"Deploy dispatched to node [{args.node_host}]: {deploy.hash.hex()}")


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnectionInfo(args.node_host, args.node_port_rpc))


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
    deploy = pycspr.create_validator_delegation(
        params=deploy_params,
        amount=int(5e11),
        public_key_of_delegator=delegator,
        public_key_of_validator=validator,
        path_to_wasm=args.path_to_wasm
        )

    return deploy


# Entry point.
if __name__ == "__main__":
    asyncio.run(_main(_ARGS.parse_args()))
