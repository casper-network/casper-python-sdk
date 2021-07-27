import argparse
import json

from pycspr.client import NodeClient
from pycspr.client import NodeConnectionInfo
from pycspr import NodeSseChannelType
from pycspr import NodeSseEventType



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
    default=NodeSseChannelType.main.name,
    dest="channel",
    help="Node event channel to which to bind - defaults to main.",
    type=str,
    choices=[i.name for i in NodeSseChannelType],
    )

# CLI argument: Type of event to which to listen to - defaults to all.
_ARGS.add_argument(
    "--event",
    default="all",
    dest="event",
    help="Type of event to which to listen to - defaults to all.",
    type=str,
    choices=["all"] + [i.name for i in NodeSseEventType],
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client = _get_client(args)

    # Bind to node events.
    client.events.get_events(
        callback=_on_event,
        channel_type = NodeSseChannelType[args.channel],
        event_type = None if args.event == "all" else NodeSseEventType[args.event],
        event_id = 0
    )


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnectionInfo(
        host=args.node_host,
        port_sse=args.node_port_sse
    ))


def _on_event(
    channel_type: NodeSseChannelType,
    event_type: NodeSseEventType,
    event_id: int,
    event_data: dict
    ):
    """Event callback handler.

    """
    print("--------------------------------------------------------------------------")
    print(f"Event #{event_id} :: {channel_type.name} :: {event_type.name}")
    print("--------------------------------------------------------------------------")
    print(json.dumps(event_data, indent=4))
    print("--------------------------------------------------------------------------")


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
