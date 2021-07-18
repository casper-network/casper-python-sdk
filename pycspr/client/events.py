import enum

from pycspr.client.connection_info import NodeConnectionInfo



class NodeEventChannelType(enum.Enum):
    """Enumeration over set of exposed node SSE channel types.
    
    """
    MAIN = enum.auto()
    SIGS = enum.auto()
    DEPLOYS = enum.auto()


class NodeEventType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.
    
    """
    API_VERSION = enum.auto()
    BLOCK_ADDED = enum.auto()
    BLOCK_FINALIZED = enum.auto()
    CONSENSUS_FINALITY_SIGNATURE = enum.auto()
    CONSENSUS_FAULT = enum.auto()
    DEPLOY_PROCESSED = enum.auto()


class EventsClient():
    """Exposes a set of functions for interacting  with a node's server sent event endpoints.
    
    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.
        
        """
        self.connection_info = connection_info
