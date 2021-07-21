import enum
import typing

from pycspr import api_v1
from pycspr.client.connection_info import NodeConnectionInfo



class NodeSseChannelType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.
    
    """
    main = enum.auto()
    deploys = enum.auto()
    sigs = enum.auto()


class NodeSseEventType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.
    
    """
    # All sub-channels.
    API_VERSION = enum.auto()

    # Main sub-channel.
    MAIN_BlockAdded = enum.auto()
    MAIN_DeployProcessed = enum.auto()
    MAIN_Fault = enum.auto()
    MAIN_Step = enum.auto()

    # Deploy sub-channel.
    DEPLOYS_DeployAccepted = enum.auto()

    # Sigs sub-channel.
    SIGNATURES_FinalitySignature = enum.auto()


class EventsClient():
    """Exposes a set of functions for interacting  with a node's server sent event endpoints.
    
    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.
        
        """
        self.connection_info = connection_info

    
    def get_events(
        self,
        callback: typing.Callable,
        channel_type: NodeSseChannelType,
        event_type: NodeSseEventType = None,
        event_id: int = 0
        ):
        """Binds to a node's event stream - events are passed to callback for processing.

        :param callback: Callback to invoke whenever an event of relevant type is received.
        :param channel_type: Type of event channel to which to bind.
        :param event_type: Type of event type to listen for (all if unspecified).
        :param event_id: Identifer of event from which to start stream listening.

        """
        api_v1.get_events(self.connection_info, callback, channel_type, event_type, event_id)
