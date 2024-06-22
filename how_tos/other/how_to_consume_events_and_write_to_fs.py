import argparse
import asyncio
import json

from pycspr import NodeEventChannel
from pycspr import NodeSseEventInfo
from pycspr import NodeSseEventType
from pycspr import NodeSseClient as NodeClient
from pycspr import NodeSseConnectionInfo as NodeConnectionInfo


# CLI argument parser.
_ARGS = argparse.ArgumentParser("How to consume node SSE events demo.")

# CLI argument: host address of target node - defaults to CCTL node 1.
_ARGS.add_argument(
    "--node-host",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API SSE port - defaults to 18101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-sse",
    default=18101,
    dest="node_port_sse",
    help="Node API SSE port.  Typically 9999 on most nodes.",
    type=int,
    )

# CLI argument: SSE channel type - defaults to main.
_ARGS.add_argument(
    "--channel",
    default=NodeEventChannel.main.name,
    dest="channel",
    help="Node event channel to which to bind - defaults to main.",
    type=str,
    choices=[i.name for i in NodeEventChannel],
    )

# CLI argument: SSE event type - defaults to all.
_ARGS.add_argument(
    "--event",
    default="all",
    dest="event",
    help="Type of event to which to listen to - defaults to all.",
    type=str,
    choices=["all"] + [i.name for i in NodeSseEventType],
    )

# CLI argument: Path to output file.
_ARGS.add_argument(
    "--output",
    dest="path_to_output",
    help="Path to output file.",
    type=str,
    )


async def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Consume Events And Write To File System")
    print("")
    print("Illustrates usage of pycspr.NodeClient.get_events function.")
    print("-" * 74)

    # Set node client.
    client = _get_client(args)

    # Write event stream to a file.
    with open(args.path_to_output, 'w') as fhandle:
        fhandle.write("[\n")
        fhandle.flush()
        try:
            client.get_events(
                ecallback=lambda x: _on_event(x, fhandle),
                echannel=NodeEventChannel[args.channel],
                etype=None if args.event == "all" else NodeSseEventType[args.event],
                eid=0
            )
        except KeyboardInterrupt:
            pass
        finally:
            fhandle.write("\n]")
            fhandle.flush()


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnectionInfo(args.node_host, args.node_port_sse))


def _on_event(event_info: NodeSseEventInfo, fhandle):
    """Event callback handler.

    """
    if event_info.idx is not None:
        fhandle.write(",\n")

    fhandle.write(json.dumps({
        "id": event_info.idx,
        "channel": event_info.channel.name,
        "payload": event_info.payload
    }, indent=4, sort_keys=True))

    fhandle.flush()


# Entry point.
if __name__ == "__main__":
    asyncio.run(_main(_ARGS.parse_args()))
