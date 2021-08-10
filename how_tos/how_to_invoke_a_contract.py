import argparse
import os
import pathlib
import random
import typing

import pycspr
from pycspr.client import NodeClient
from pycspr.client import NodeConnectionInfo
from pycspr.crypto import KeyAlgorithm
from pycspr.factory.cl import create_cl_type_of_simple
from pycspr.factory.cl import create_cl_value
from pycspr.types import CLTypeKey
from pycspr.types import Deploy
from pycspr.types import DeployParameters
from pycspr.types import ExecutableDeployItem_ModuleBytes
from pycspr.types import ExecutableDeployItem_StoredContractByHash
from pycspr.types import PrivateKey
from pycspr.types import PublicKey
from pycspr.utils import io as _io



# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to install an ERC-20 smart contract.")

# CLI argument: path to contract operator secret key - defaults to NCTL faucet.
_ARGS.add_argument(
    "--operator-secret-key-path",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "faucet" / "secret_key.pem",
    dest="path_to_operator_secret_key",
    help="Path to operator's secret_key.pem file.",
    type=str,
    )

# CLI argument: type of contract operator secret key - defaults to ED25519.
_ARGS.add_argument(
    "--operator-secret-key-type",
    default=KeyAlgorithm.ED25519.name,
    dest="type_of_operator_secret_key",
    help="Type of operator's secret key.",
    type=str,
    )

# CLI argument: path to user to whom tokens will be transferred - defaults to NCTL user 1.
_ARGS.add_argument(
    "--user-public-key-path",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "users" / "user-1" / "public_key_hex",
    dest="path_to_user_public_key",
    help="Path to user's public_key_hex file.",
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

# CLI argument: amount in motes to be offered as payment.
_ARGS.add_argument(
    "--payment",
    default=int(1e9),
    dest="deploy_payment",
    help="Amount in motes to be offered as payment.",
    type=int,
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

# CLI argument: amount of ERC-20 tokens to be transferred to user..
_ARGS.add_argument(
    "--amount",
    default=int(2e9),
    dest="amount",
    help="Amount of ERC-20 tokens to be transferred to user.",
    type=int,
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client: NodeClient = _get_client(args)

    # Set contract operator / user.
    operator, user = _get_operator_and_user_keys(args)

    # Set contract hash.
    contract_hash: bytes = _get_contract_hash(args, client, operator)

    # Set deploy.
    deploy: Deploy = _get_deploy(args, contract_hash, operator, user)

    # Approve deploy.
    deploy.approve(operator)

    # Dispatch deploy to a node.
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


def _get_operator_and_user_keys(args: argparse.Namespace) -> typing.Tuple[PrivateKey, PublicKey]:
    """Returns the smart contract operator's private key.

    """
    print(args.path_to_user_public_key)

    operator = pycspr.factory.parse_private_key(
        args.path_to_operator_secret_key,
        args.type_of_operator_secret_key,
        )
    user = pycspr.factory.parse_public_key(
        args.path_to_user_public_key,
        )

    return operator, user


def _get_contract_hash(args: argparse.Namespace, client: NodeClient, operator: PrivateKey) -> bytes:
    """Returns on-chain contract identifier.

    """
    pass


def _get_deploy(args: argparse.Namespace, contract_hash: bytes, operator: PrivateKey, user:PublicKey) -> Deploy:
    """Returns delegation deploy to be dispatched to a node.

    """
    # Set standard deploy parameters.
    params: DeployParameters = \
        pycspr.factory.create_deploy_parameters(
            account=operator,
            chain_name=args.chain_name
            )

    # Set payment logic.
    payment: ExecutableDeployItem_ModuleBytes = \
        pycspr.factory.create_standard_payment(args.deploy_payment)

    # Set session logic.
    session: ExecutableDeployItem_StoredContractByHash = ExecutableDeployItem_StoredContractByHash(
        entry_point="transfer",
        hash=contract_hash,
        args = [
            pycspr.create_deploy_argument(
                "amount",
                args.amount,
                create_cl_type_of_simple(CLTypeKey.U256)
                ),
        ]
    )

    return pycspr.create_deploy(params, payment, session)


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
