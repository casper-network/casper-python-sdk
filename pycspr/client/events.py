import enum
import requests
import sseclient
from json import loads
from typing import Callable
from typing import Generator
from typing import Tuple

from pycspr.api import NodeConnectionInfo


class NodeSseChannelType(enum.Enum):
    """ Enumeration over set of exposed node SEE event types. """
    deploys = enum.auto()
    main = enum.auto()
    sigs = enum.auto()


class NodeSseEventType(enum.Enum):
    """ Enumeration over set of exposed node SEE event types. """
    ApiVersion = enum.auto()
    BlockAdded = enum.auto()
    DeployAccepted = enum.auto()
    DeployProcessed = enum.auto()
    Fault = enum.auto()
    FinalitySignature = enum.auto()
    Step = enum.auto()


# Map: channel type <-> event type.
_CHANNEL_TO_TYPE = {
    NodeSseChannelType.deploys: {
        NodeSseEventType.ApiVersion,
        NodeSseEventType.DeployAccepted
    },
    NodeSseChannelType.main: {
        NodeSseEventType.ApiVersion,
        NodeSseEventType.BlockAdded,
        NodeSseEventType.DeployProcessed,
        NodeSseEventType.Fault,
        NodeSseEventType.Step
    },
    NodeSseChannelType.sigs: {
        NodeSseEventType.ApiVersion,
        NodeSseEventType.FinalitySignature
    }
}


class EventsClient:
    """ Bind to a node's event stream. """

    def __init__(self, node: NodeConnectionInfo):
        """
        Constructor EventChannel.

        :param node: Information required to connect to a node.
        """
        self._node = node

    def get_events(self, callback: Callable, channel_type: NodeSseChannelType,
                   event_type: NodeSseEventType, event_id: int = 0) -> None:
        """
        Binds to a node's event stream - events are passed to callback for
        processing.

        :param callback: Callback to invoke whenever an event of relevant type
                         is received.
        :param channel_type: Type of event channel to which to bind.
        :param event_type: Type of event type to listen for
                           (all if unspecified).
        :param event_id: Identifer of event from which to start stream
                         listening.
        """
        # validate that the channel supports the event type.
        if channel_type not in _CHANNEL_TO_TYPE:
            raise ValueError(f"Unsupported SSE channel: {channel_type.name}.")

        if event_type not in _CHANNEL_TO_TYPE[channel_type]:
            raise ValueError(f"Unsupported SSE channel/event permutation: "
                             f"{channel_type.name}:{event_type.name}.")

        # get and set sse clieant
        params = f"?start_from={event_id}" if event_id else ""
        url = f"{self._node.address_sse}/{channel_type.name.lower()}{params}"
        stream = requests.get(url, stream=True)
        self._sse_client = sseclient.SSEClient(stream)

        for event_type, event_id, payload in self._yield_events(self):
            callback(self._channel_type, event_type, event_id, payload)

    def _yield_events(self) -> Generator:
        """ Yields events streaming from node.  """
        try:
            for event in self._sse_client.events():
                parsed = self._parse_event(event.id, loads(event.data))
                if parsed:
                    yield parsed
        except Exception as err:
            try:
                self._sse_client.close()
            finally:
                raise err

    def _parse_event(self, event_id: int, payload: dict
                     ) -> Tuple[NodeSseEventType, int, dict]:
        """ Parses raw event data for upstream processing.  """
        events = {
                "ApiVersion": NodeSseEventType.ApiVersion,
                "BlockAdded": NodeSseEventType.BlockAdded,
                "DeployProcessed": NodeSseEventType.DeployProcessed,
                "Fault": NodeSseEventType.Fault,
                "Step": NodeSseEventType.Step,
                "DeployAccepted": NodeSseEventType.DeployAccepted,
                "FinalitySignature": NodeSseEventType.FinalitySignature
        }
        for event_name in events:
            if event_name in payload:
                return events.get(event_name), event_id, payload
        # @TODO: process unkown event_type
        print(f"Unknown event occured. even_id: {event_id}\n"
              f"payload: {payload}")
        return None
