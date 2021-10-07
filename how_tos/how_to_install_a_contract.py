import argparse
import os
import pathlib

import pycspr
from pycspr.client import NodeClient
from pycspr.client import NodeConnectionInfo
from pycspr.crypto import KeyAlgorithm
from pycspr.types import Deploy
from pycspr.types import DeployParameters
from pycspr.types import ExecutableDeployItem_ModuleBytes
from pycspr.types import PrivateKey



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

# CLI argument: path to smart contract wasm binary - defaults to NCTL bin/eco/erc20.wasm.
_ARGS.add_argument(
    "--path-to-wasm",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "bin" / "eco" / "erc20.wasm",
    dest="path_to_wasm",
    help="Path to erc20.wasm file.",
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
    default=int(50e9),
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

# CLI argument: number of decimal places within ERC-20 token to be minted.
_ARGS.add_argument(
    "--decimals",
    default=11,
    dest="token_decimals",
    help="Number of decimal places within ERC-20 token to be minted.",
    type=int,
    )

# CLI argument: name of ERC-20 token to be minted.
_ARGS.add_argument(
    "--name",
    default="Acme Token",
    dest="token_name",
    help="Name of ERC-20 token to be minted.",
    type=str,
    )

# CLI argument: Total number of ERC-20 tokens to be issued.
_ARGS.add_argument(
    "--supply",
    default=1e15,
    dest="token_total_supply",
    help="Total number of ERC-20 tokens to be issued.",
    type=int,
    )

# CLI argument: symbol of ERC-20 token to be minted.
_ARGS.add_argument(
    "--symbol",
    default="ACME",
    dest="token_symbol",
    help="Symbol of ERC-20 token to be minted.",
    type=str,
    )



def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client = _get_client(args)

    # Set contract operator.
    operator = _get_operator_key(args)

    # Set deploy.
    deploy: Deploy = _get_deploy(args, operator)

    # Approve deploy.
    deploy.approve(operator)

    # Dispatch deploy to a node.
    client.deploys.send(deploy)

    print("-------------------------------------------------------------------------------------------------------")
    print(f"Deploy dispatched to node [{args.node_host}]: {deploy.hash.hex()}")
    print("-------------------------------------------------------------------------------------------------------")


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnectionInfo(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    ))


def _get_operator_key(args: argparse.Namespace) -> PrivateKey:
    """Returns the smart contract operator's private key.

    """
    return pycspr.parse_private_key(
        args.path_to_operator_secret_key,
        args.type_of_operator_secret_key,
        )


def _get_deploy(args: argparse.Namespace, operator: PrivateKey) -> Deploy:
    """Returns delegation deploy to be dispatched to a node.

    """
    # Set standard deploy parameters.
    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=operator,
            chain_name=args.chain_name
            )

    # Set payment logic.
    payment: ExecutableDeployItem_ModuleBytes = \
        pycspr.create_standard_payment(args.deploy_payment)

    # Set session logic.
    session: ExecutableDeployItem_ModuleBytes = ExecutableDeployItem_ModuleBytes(
        module_bytes=pycspr.read_wasm(args.path_to_wasm),
        args = [
            pycspr.create_deploy_arg(
                "token_decimals",
                pycspr.cl_value.u8(args.token_decimals)
                ),
            pycspr.create_deploy_arg(
                "token_name",
                pycspr.cl_value.string(args.token_name)
                ),
            pycspr.create_deploy_arg(
                "token_symbol",
                pycspr.cl_value.string(args.token_symbol)
                ),
            pycspr.create_deploy_arg(
                "token_total_supply",
                pycspr.cl_value.u256(args.token_total_supply)
                ),
        ]
    )

    return pycspr.create_deploy(params, payment, session)


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
