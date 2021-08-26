from pycspr.client.connection import NodeConnectionInfo
from pycspr.client.deploys    import DeploysClient as _DeploysClient
from pycspr.client.events     import EventsClient as _EventsClient
from pycspr.client.events     import NodeSseChannelType
from pycspr.client.events     import NodeSseEventType
from pycspr.client.queries    import QueriesClient as _QueriesClient
from pycspr.api.constants     import REST_ENDPOINTS as NODE_REST_ENDPOINTS
from pycspr.api.constants     import RPC_ENDPOINTS as NODE_RPC_ENDPOINTS
from pycspr.api.constants     import SSE_ENDPOINTS as NODE_SSE_ENDPOINTS



class NodeClient():
    """Exposes a set of (categorised) functions for interacting  with a node.
    
    """
    NODE_REST_ENDPOINTS: set = NODE_REST_ENDPOINTS
    NODE_RPC_ENDPOINTS: set = NODE_RPC_ENDPOINTS
    NODE_SSE_ENDPOINTS: set = NODE_SSE_ENDPOINTS

    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.
        
        """
        self.deploys = _DeploysClient(connection_info)
        self.events = _EventsClient(connection_info)
        self.queries = _QueriesClient(connection_info)
