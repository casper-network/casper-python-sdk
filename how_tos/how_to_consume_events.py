import argparse
import os
import pathlib
import random
import typing

import pycspr
from pycspr.types import PrivateKey
from pycspr.types import Deploy
from pycspr.types import NodeSseChannelType
from pycspr.types import NodeSseEventType


# CHANNELS / EVENTS
# main
# main:ApiVersion
# main:BlockAdded
# main:DeployProcessed
# main:Fault
# main:Step
#
# deploys
# deploys:DeployAccepted
#
# sigs
# sigs:FinalitySignature


# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to consume SSE events emitted by a node.")

# CLI argument: host address of target node - defaults to NCTL node 1.
_ARGS.add_argument(
    "--node-host",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API SSE port - defaults to 18101 @ NCTL node 1.
_ARGS.add_argument(
    "--node-port-sse",
    default=18101,
    dest="node_port_sse",
    help="Node API SSE port.  Typically 9999 on most nodes.",
    type=int,
    )

# CLI argument: Node API SSE port - defaults to 18101 @ NCTL node 1.
_ARGS.add_argument(
    "--channel",
    default="main",
    dest="channel",
    help="Node event channel to which to bind - defaults to main.",
    type=str,
    choices=("main", "deploys", "sigs"),
    )

# CLI argument: Type of event to which to listen to - defaults to all.
_ARGS.add_argument(
    "--event",
    default="*",
    dest="event_type",
    help="Type of event to which to listen to - defaults to all.",
    type=str,
    choices=("*", "ApiVersion", "BlockAdded", "DeployProcessed", "Fault", "Step", "DeployAccepted", "FinalitySignature"),
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set client.
    client = _get_client(args)

    client.events.get_events(
        callback=_on_event,
        channel_type = NodeSseChannelType[args.channel],
        event_type = None if args.event_type == "*" else NodeSseEventType[args.event_type],
        event_id = 0
    )


def _get_client(args: argparse.Namespace) -> pycspr.NodeClient:
    """Returns a pycspr client instance.

    """
    connection = pycspr.NodeConnectionInfo(
        host=args.node_host,
        port_sse=args.node_port_sse
    )

    return pycspr.NodeClient(connection)


def _on_event(event_type, event_id: int, event_data: dict):
    """Event callback handler.

    """
    print(event_type, event_id, event_data)


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
