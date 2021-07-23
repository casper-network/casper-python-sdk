import json
import typing

import requests
import sseclient

from pycspr.types import NodeConnectionInfo
from pycspr.types import NodeSseChannelType
from pycspr.types import NodeSseEventType



def execute(
    connection_info: NodeConnectionInfo,
    callback: typing.Callable,
    channel_type: NodeSseChannelType,
    event_type: NodeSseEventType = None,
    event_id: int = 0
    ):
    """Binds to a node's event stream - events are passed to callback for processing.

    :param connection_info: Information required to connect to a node.
    :param callback: Callback to invoke whenever an event of relevant type is received.
    :param channel_type: Type of event channel to which to bind.
    :param event_type: Type of event type to listen for (all if unspecified).
    :param event_id: Identifer of event from which to start stream listening.

    """
    assert isinstance(callback, typing.Callable)
    assert isinstance(event_id, int)

    sse_client = _get_sse_client(connection_info, channel_type, event_id)
    for event_type, event_id, payload in _yield_events(sse_client):
        callback(event_type, event_id, payload)


def _get_sse_client(connection_info: NodeConnectionInfo, channel_type: NodeSseChannelType, event_id: int):
    """Returns SSE client.

    """
    url = _get_sse_url(connection_info, channel_type, event_id)
    stream = requests.get(url, stream=True)
    return sseclient.SSEClient(stream)


def _get_sse_url(connection_info: NodeConnectionInfo, channel_type: NodeSseChannelType, event_id: int) -> str:
    """Returns URL of SSE endpoint to which to bind.

    """
    url = f"{connection_info.address_sse}/main"
    if event_id:
        url = f"{url}?start_from={event_id}"

    return url    


def _parse_event(event_id: int, payload: dict) -> typing.Tuple[NodeSseEventType, int, dict]:
    """Parses raw event data for upstream processing.

    """
    if 'ApiVersion' in payload:
        pass

    elif 'BlockAdded' in payload:
        return \
            NodeSseEventType.MAIN_BlockAdded, \
            event_id, \
            payload

    elif 'DeployProcessed' in payload:
        return \
            NodeSseEventType.MAIN_DeployProcessed, \
            event_id, \
            payload

    elif 'Fault' in payload:
        return \
            NodeSseEventType.MAIN_Fault, \
            event_id, \
            payload

    elif 'Step' in payload:
        return \
            NodeSseEventType.MAIN_Step, \
            event_id, \
            payload

    elif 'DeployAccepted' in payload:
        return \
            NodeSseEventType.DEPLOYS_DeployAccepted, \
            event_id, \
            payload

    elif 'FinalitySignature' in payload:
        return \
            NodeSseEventType.SIGNATURES_FinalitySignature, \
            event_id, \
            payload

    else:
        print("TODO: process unknown event: {payload}")


def _yield_events(sse_client) -> typing.Generator:
    """Yields events streaming from node.

    """
    try:
        for event in sse_client.events():
            parsed = _parse_event(event.id, json.loads(event.data))
            if parsed:
                yield parsed
    except Exception as err:
        try:
            sse_client.close()
        except:
            pass
        finally:
            raise err
