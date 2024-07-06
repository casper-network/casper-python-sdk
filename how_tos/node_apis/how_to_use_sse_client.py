import argparse
import asyncio
import json
import typing

from pycspr import NodeSseEventType
from pycspr import NodeSseEventInfo
from pycspr import NodeRestClient
from pycspr import NodeRestConnectionInfo
from pycspr import NodeSseClient
from pycspr import NodeSseConnectionInfo


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

# CLI argument: Node API REST port - defaults to 11101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rest",
    default=13101,
    dest="node_port_rest",
    help="Node API JSON-RPC port.  Typically 8888 on most nodes.",
    type=int,
    )

# CLI argument: Node API SSE port - defaults to 14101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-sse",
    default=14101,
    dest="node_port_sse",
    help="Node API SSE port.  Typically 9999 on most nodes.",
    type=int,
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


async def main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Consume Node SSE API")
    print("-" * 74)

    # Parse arg: event type.
    etype = NodeSseEventType.All if args.event == "all" else NodeSseEventType[args.event]

    # Set node clients.
    sse_client, rest_client = _get_clients(args)

    # Bind to event stream.
    print("pycspr.NodeSseClient.yield_events :: binding to event stream ...")
    event_count = 0
    for einfo in sse_client.yield_events(etype, 0):
        print(f"\tEvent Id = {einfo.idx} :: Event Type = {einfo.typeof}")
        event_count += 1
        if event_count == 5:
            break

    # Await until 2 blocks have been added to linear chain.
    print("pycspr.NodeSseClient.await_n_blocks :: awaiting 2 blocks ...")
    block_height = await rest_client.get_block_height()
    await sse_client.await_n_blocks(2)
    assert await rest_client.get_block_height() == block_height + 2

    # Await next era.
    print("pycspr.NodeSseClient.await_n_eras :: awaiting 1 era ...")
    era_height = await rest_client.get_era_height()
    await sse_client.await_n_eras(1)
    assert await rest_client.get_era_height() == era_height + 1

    # Listen to node events.
    print("pycspr.NodeSseClient.get_events :: listen to events and handoff to callback handler ...")
    sse_client.get_events(etype, 0, _on_event_callback)

    print("-" * 74)


def _get_clients(args: argparse.Namespace) -> typing.Tuple[NodeSseClient, NodeRestClient]:
    """Returns SSE & REST client instances.

    """
    return \
        NodeSseClient(
            NodeSseConnectionInfo(
                args.node_host,
                args.node_port_sse
            )
        ), \
        NodeRestClient(
            NodeRestConnectionInfo(
                args.node_host,
                args.node_port_rest
            )
        )


def _on_event_callback(event_info: NodeSseEventInfo):
    """Event callback handler.

    """
    print("-" * 74)
    print(f"Event #{event_info.idx or 0} :: {event_info.typeof}")
    print("-" * 74)
    print(json.dumps(event_info.payload, indent=4))
    print("-" * 74)


# Entry point.
if __name__ == "__main__":
    asyncio.run(main(_ARGS.parse_args()))
