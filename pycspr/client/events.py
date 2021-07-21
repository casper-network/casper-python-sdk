import enum

from pycspr.client.connection_info import NodeConnectionInfo



class NodeEventType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.
    
    """
    # Main sub-channel.
    API_VERSION = enum.auto()
    MAIN_BlockAdded = enum.auto()
    MAIN_DeployProcessed = enum.auto()
    MAIN_Fault = enum.auto()
    MAIN_Step = enum.auto()

    # Deploy sub-channel.
    DEPLOYS_DeployAccepted = enum.auto()

    # Sigs sub-channel.
    SIGNATURES_FinalitySignature = enum.auto()

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
