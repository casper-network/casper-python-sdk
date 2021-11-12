import argparse
import json

from pycspr import NodeClient
from pycspr import NodeConnection
from pycspr import NodeEventChannelType
from pycspr import NodeEventType


# CLI argument parser.
_ARGS = argparse.ArgumentParser("How to consume node SSE events demo.")

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
    default=NodeEventChannelType.main.name,
    dest="channel",
    help="Node event channel to which to bind - defaults to main.",
    type=str,
    choices=[i.name for i in NodeEventChannelType],
    )

# CLI argument: Type of event to which to listen to - defaults to all.
_ARGS.add_argument(
    "--event",
    default="all",
    dest="event",
    help="Type of event to which to listen to - defaults to all.",
    type=str,
    choices=["all"] + [i.name for i in NodeEventType],
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client = _get_client(args)

    # Bind to node events.
    client.get_events(
        callback=_on_event,
        channel_type=NodeEventChannelType[args.channel],
        event_type=None if args.event == "all" else NodeEventType[args.event],
        event_id=0
    )


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_sse=args.node_port_sse
    ))


def _on_event(
    channel_type: NodeEventChannelType,
    event_type: NodeEventType,
    event_id: int,
    event_data: dict
):
    """Event callback handler.

    """
    print("-" * 74)
    print(f"Event #{event_id} :: {channel_type.name} :: {event_type.name}")
    print("-" * 74)
    print(json.dumps(event_data, indent=4))
    print("-" * 74)


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
