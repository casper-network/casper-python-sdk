import json
import typing

from pycspr.api.constants import SSE_CHANNEL_TO_SSE_EVENT
from pycspr.api.constants import NodeEventType
from pycspr.api.constants import NodeEventChannelType
from pycspr.api.connection import NodeConnection


def get_events(
    node: NodeConnection,
    callback: typing.Callable,
    channel_type: NodeEventChannelType,
    event_type: NodeEventType = None,
    event_id: int = 0
):
    """Binds to a node's event stream - events are passed to callback for processing.

    :param node: Information required to connect to a node.
    :param callback: Callback to invoke whenever an event of relevant type is received.
    :param channel_type: Type of event channel to which to bind.
    :param event_type: Type of event type to listen for (all if unspecified).
    :param event_id: Identifer of event from which to start stream listening.

    """
    if event_type is not None:
        _validate_that_channel_supports_event_type(channel_type, event_type)

    sse_client = node.get_sse_client(channel_type, event_id)
    for event_type, event_id, payload in _yield_events(sse_client):
        callback(channel_type, event_type, event_id, payload)


def _parse_event(event_id: int, payload: dict) -> typing.Tuple[NodeEventType, int, dict]:
    """Parses raw event data for upstream processing.

    """
    if "ApiVersion" in payload:
        pass

    elif "BlockAdded" in payload:
        return \
            NodeEventType.BlockAdded, \
            event_id, \
            payload

    elif "DeployProcessed" in payload:
        return \
            NodeEventType.DeployProcessed, \
            event_id, \
            payload

    elif "Fault" in payload:
        return \
            NodeEventType.Fault, \
            event_id, \
            payload

    elif "Step" in payload:
        return \
            NodeEventType.Step, \
            event_id, \
            payload

    elif "DeployAccepted" in payload:
        return \
            NodeEventType.DeployAccepted, \
            event_id, \
            payload

    elif "FinalitySignature" in payload:
        return \
            NodeEventType.FinalitySignature, \
            event_id, \
            payload

    else:
        print("TODO: process unknown event: {payload}")


def _validate_that_channel_supports_event_type(
    channel_type: NodeEventChannelType,
    event_type: NodeEventType = None
):
    """Validates that the channel supports the event type.

    """
    if channel_type not in SSE_CHANNEL_TO_SSE_EVENT:
        raise ValueError(f"Unsupported SSE channel: {channel_type.name}.")

    if event_type not in SSE_CHANNEL_TO_SSE_EVENT[channel_type]:
        raise ValueError(f"Unsupported channel/event: {channel_type.name}:{event_type.name}.")


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
        except Exception as inner_err:
            print(inner_err)
        finally:
            raise err
