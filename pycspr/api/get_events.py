import json
import typing

import requests
import sseclient

import pycspr
from pycspr.types.node import NodeEventType



def execute(event_callback: typing.Callable, event_id: int = 0):
    """Binds to a node's event stream - events are passed to callback for processing.

    :param event_callback: Callback to invoke whenever an event of relevant type is received.
    :param event_id: Identifer of event from which to start stream.

    """
    assert isinstance(event_callback, typing.Callable)
    assert isinstance(event_id, int)

    for event_type, event_id, payload in _yield_events(event_id):
        event_callback(event_type, event_id, payload)


def _yield_events(event_id: int) -> typing.Generator:
    """Yields events streaming from node.

    """
    url = pycspr.CONNECTION.address_sse
    if event_id:
        url = f"{url}?start_from={event_id}"

    stream = requests.get(url, stream=True)
    client = sseclient.SSEClient(stream)

    try:
        for event in client.events():
            parsed = _parse_event(event.id, json.loads(event.data))
            if parsed:
                yield parsed
    except Exception as err:
        try:
            client.close()
        except:
            pass
        finally:
            raise err


def _parse_event(
    event_id: int,
    payload: dict,
    ) -> typing.Tuple[NodeEventType, int, dict]:
    """Parses raw event data for upstream processing.

    """
    if 'ApiVersion' in payload:
        pass

    elif 'BlockAdded' in payload:
        return \
            NodeEventType.BLOCK_ADDED, \
            event_id, \
            payload

    elif 'BlockFinalized' in payload:
        return \
            NodeEventType.BLOCK_FINALIZED, \
            event_id, \
            payload

    elif 'FinalitySignature' in payload:
        return \
            NodeEventType.CONSENSUS_FINALITY_SIGNATURE, \
            event_id, \
            payload

    elif 'Fault' in payload:
        return \
            NodeEventType.CONSENSUS_FAULT, \
            event_id, \
            payload

    elif 'DeployProcessed' in payload:
        return \
            NodeEventType.DEPLOY_PROCESSED, \
            event_id, \
            payload

    else:
        print("TODO: process unknown event: {payload}")
