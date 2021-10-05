from pycspr.api import CasperApi
from pycspr.api import NodeConnectionInfo
from pycspr.client.deploys import DeploysClient
from pycspr.client.events import EventsClient
from pycspr.client.queries import QueriesClient
from pycspr.api.constants import REST_ENDPOINTS
from pycspr.api.constants import RPC_ENDPOINTS
from pycspr.api.constants import SSE_ENDPOINTS


class NodeClient:
    # @TODO: Why? Here?
    NODE_REST_ENDPOINTS: set = REST_ENDPOINTS
    NODE_RPC_ENDPOINTS: set = RPC_ENDPOINTS
    NODE_SSE_ENDPOINTS: set = SSE_ENDPOINTS

    def __init__(self, connection_info: NodeConnectionInfo):
        self._api = CasperApi(connection_info)
        # base Client
        self.queries = QueriesClient(self._api)
        # special client
        self.deploys = DeploysClient(self.queries)

        # @TODO: Events better design. ?put sseclient in CasperApi?
        self.events = EventsClient(connection_info)
