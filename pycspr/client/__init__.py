from pycspr.api import NodeConnectionInfo
from pycspr.client.deploys import DeploysClient
from pycspr.client.events import EventsClient
from pycspr.client.queries import QueriesClient
from pycspr.api.constants import REST_ENDPOINTS
from pycspr.api.constants import RPC_ENDPOINTS
from pycspr.api.constants import SSE_ENDPOINTS


class NodeClient():
    """
    Exposes a set of (categorised) functions for interacting  with a node.
    """
    NODE_REST_ENDPOINTS: set = REST_ENDPOINTS
    NODE_RPC_ENDPOINTS: set = RPC_ENDPOINTS
    NODE_SSE_ENDPOINTS: set = SSE_ENDPOINTS

    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.deploys = DeploysClient(connection_info)
        self.events = EventsClient(connection_info)
        self.queries = QueriesClient(connection_info)
