import typing

from pycspr import api_v1
from pycspr.types import NodeConnectionInfo
from pycspr.types import NodeEventType
from pycspr.types import NODE_REST_ENDPOINTS
from pycspr.types import NODE_RPC_ENDPOINTS
from pycspr.types import NODE_SSE_ENDPOINTS



class NodeClient():
    """Exposes a set of functions for interacting  with a node.
    
    """

    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.
        
        """
        self.connection_info = connection_info
        self.NODE_REST_ENDPOINTS = NODE_REST_ENDPOINTS
        self.NODE_RPC_ENDPOINTS = NODE_RPC_ENDPOINTS
        self.NODE_SSE_ENDPOINTS = NODE_SSE_ENDPOINTS
    

    def get_account_balance(
        self,
        purse_uref: str,
        state_root_hash: typing.Union[bytes, None] = None,
        ) -> int:
        """Returns account balance at a certain global state root hash.

        :param purse_uref: URef of a purse associated with an on-chain account.
        :param state_root_hash: A node's root state hash at some point in chain time.
        :returns: Account balance if on-chain account is found.

        """
        return api_v1.get_account_balance(self.connection_info, purse_uref, state_root_hash)


    def get_account_info(
        self,
        account_hash: bytes,
        state_root_hash: typing.Union[bytes, None] = None
        ) -> dict:
        """Returns account information at a certain global state root hash.

        :param account_hash: An on-chain account identifier derived from it's associated public key.
        :param state_root_hash: A node's root state hash at some point in chain time.
        :param parse_response: Flag indicating whether to parse web-service response.

        :returns: Account information in JSON format.

        """
        return api_v1.get_account_info(self.connection_info, account_hash, state_root_hash)


    def get_account_main_purse_uref(
        self,
        account_key: bytes,
        state_root_hash: typing.Union[bytes, None] = None,
        ) -> str:
        """Returns an on-chain account's main purse unforgeable reference.

        :param account_key: Key of an on-chain account.
        :param state_root_hash: A node's root state hash at some point in chain time.
        :returns: Account main purse unforgeable reference.

        """
        return api_v1.get_account_main_purse_uref(self.connection_info, account_key, state_root_hash)


    def get_auction_info(self) -> dict:
        """Returns current auction system contract information.

        :returns: Current auction system contract information.

        """
        return api_v1.get_auction_info(self.connection_info)


    def get_block(self, block_id: typing.Union[None, str, int] = None) -> dict:
        """Returns on-chain block information.

        :param block_id: Identifier of a finialised block.
        :returns: On-chain block information.

        """
        return api_v1.get_block(self.connection_info, block_id)


    def get_block_at_era_switch(
        self,
        polling_interval_seconds: float = 1.0,
        max_polling_time_seconds: float = 120.0
        ) -> dict:
        """Returns last finialised block in current era.

        :param polling_interval_seconds: Time interval time (in seconds) before polling for next switch block.
        :param max_polling_time_seconds: Maximum time in seconds to poll.
        :returns: On-chain block information.

        """
        return api_v1.get_block_at_era_switch(self.connection_info, polling_interval_seconds, max_polling_time_seconds)


    def get_block_transfers(self, block_id: typing.Union[None, str, int] = None) -> typing.Tuple[str, list]:
        """Returns on-chain block transfers information.

        :param block_id: Identifier of a finialised block.
        :returns: On-chain block transfers information.

        """
        return api_v1.get_block_transfers(self.connection_info, block_id)


    def get_node_metrics(self) -> list:
        """Returns set of node metrics.

        :returns: Node metrics information.

        """
        return api_v1.get_node_metrics(self.connection_info)


    def get_node_metric(self, metric_id: str) -> list:
        """Returns node metrics information filtered by a particular metric.

        :param metric_id: Identifier of node metric.
        :returns: Node metrics information filtered by a particular metric.

        """
        return api_v1.get_node_metrics(self.connection_info, metric_id)


    def get_node_peers(self) -> dict:
        """Returns node peers information.

        :returns: Node peers information.

        """
        return api_v1.get_node_peers(self.connection_info)


    def get_node_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.

        """
        return api_v1.get_node_status(self.connection_info)


    def get_rpc_endpoint(self, endpoint: str = None) -> dict:
        """Returns RPC schema.

        :param endpoint: A specific endpoint of interest.
        :returns: Either list of all RPC endpoints or RPC schema endpoint fragment.

        """
        return api_v1.get_rpc_endpoint(self.connection_info, endpoint)


    def get_rpc_endpoints(self) -> typing.Union[dict, list]:
        """Returns RPC schema.

        :param endpoint: A specific endpoint of interest.
        :returns: Either list of all RPC endpoints or RPC schema endpoint fragment.

        """
        return api_v1.get_rpc_endpoint(self.connection_info)


    def get_rpc_schema(self) -> dict:
        """Returns RPC schema.

        :returns: Node RPC API schema.

        """
        return api_v1.get_rpc_schema(self.connection_info)


    def get_state_root_hash(self, block_id: typing.Union[None, str, int] = None) -> bytes:
        """Returns an root hash of global state at a specified block.

        :param block_id: Identifier of a finialised block.
        :returns: State root hash at specified block.

        """
        return bytes.fromhex(
            api_v1.get_state_root_hash(self.connection_info, block_id)
        )

