import typing

from pycspr import api
from pycspr import types
from pycspr.client import NodeConnectionInfo



class QueriesClient():
    """Exposes a set of functions for interacting  with a node.
    
    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.
        
        """
        self.connection_info = connection_info


    def get_account_balance(self, purse_uref: str, state_root_hash: typing.Union[bytes, None] = None) -> int:
        """Returns account balance at a certain global state root hash.

        :param purse_uref: URef of a purse associated with an on-chain account.
        :param state_root_hash: A node's root state hash at some point in chain time, if none then defaults to the most recent.
        :returns: Account balance if on-chain account is found.

        """
        state_root_hash = state_root_hash or self.get_state_root_hash()
    
        return api.get_account_balance(self.connection_info, purse_uref, state_root_hash)


    def get_account_info(self, account_key: bytes, block_id: types.OptionalBlockIdentifer = None) -> dict:
        """Returns account information at a certain global state root hash.

        :param account_key: An account holder's public key prefixed with a key type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.

        """
        return api.get_account_info(self.connection_info, account_key, block_id)


    def get_account_main_purse_uref(
        self,
        account_key: bytes,
        block_id: types.OptionalBlockIdentifer = None
        ) -> types.UnforgeableReference:
        """Returns an on-chain account's main purse unforgeable reference.

        :param account_key: Key of an on-chain account.
        :param block_id: Identifier of a finalised block.
        :returns: Account main purse unforgeable reference.

        """
        return api.get_account_main_purse_uref(self.connection_info, account_key, block_id)


    def get_auction_info(self, block_id: types.OptionalBlockIdentifer = None) -> dict:
        """Returns current auction system contract information.

        :returns: Current auction system contract information.

        """
        return api.get_auction_info(self.connection_info, block_id)


    def get_block(self, block_id: types.OptionalBlockIdentifer = None) -> dict:
        """Returns on-chain block information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block information.

        """
        return api.get_block(self.connection_info, block_id)


    def get_block_at_era_switch(self, polling_interval_seconds: float = 1.0, max_polling_time_seconds: float = 120.0) -> dict:
        """Returns last finalised block in current era.

        :param polling_interval_seconds: Time interval time (in seconds) before polling for next switch block.
        :param max_polling_time_seconds: Maximum time in seconds to poll.
        :returns: On-chain block information.

        """
        return api.get_block_at_era_switch(self.connection_info, polling_interval_seconds, max_polling_time_seconds)


    def get_block_transfers(self, block_id: types.OptionalBlockIdentifer = None) -> typing.Tuple[str, list]:
        """Returns on-chain block transfers information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block transfers information.

        """
        return api.get_block_transfers(self.connection_info, block_id)


    def get_deploy(self, deploy_id: typing.Union[bytes, str]) -> dict:
        """Returns on-chain deploy information.

        :param deploy_id: Identifier of a finalised block.
        :returns: On-chain deploy information.

        """
        return api.get_deploy(self.connection_info, deploy_id)


    def get_dictionary_item(self, identifier: types.DictionaryIdentifier) -> dict:
        """Returns on-chain data stored under a dictionary item.

        :param identifier: Identifier required to query a dictionary item.
        :returns: On-chain data stored under a dictionary item.

        """
        return api.get_dictionary_item(self.connection_info, identifier)


    def get_era_info(self, block_id: types.OptionalBlockIdentifer = None) -> dict:
        """Returns current era information.

        :param block_id: Identifier of a finalised block.
        :returns: Era information.

        """
        return api.get_era_info(self.connection_info, block_id)


    def get_node_metrics(self) -> list:
        """Returns set of node metrics.

        :returns: Node metrics information.

        """
        return api.get_node_metrics(self.connection_info)


    def get_node_metric(self, metric_id: str) -> list:
        """Returns node metrics information filtered by a particular metric.

        :param metric_id: Identifier of node metric.
        :returns: Node metrics information filtered by a particular metric.

        """
        return api.get_node_metrics(self.connection_info, metric_id)


    def get_node_peers(self) -> dict:
        """Returns node peers information.

        :returns: Node peers information.

        """
        return api.get_node_peers(self.connection_info)


    def get_node_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.

        """
        return api.get_node_status(self.connection_info)


    def get_rpc_endpoint(self, endpoint: str) -> dict:
        """Returns RPC schema.

        :param endpoint: A specific endpoint of interest.
        :returns: A JSON-RPC schema endpoint fragment.

        """
        return api.get_rpc_endpoint(self.connection_info, endpoint)


    def get_rpc_endpoints(self) -> typing.Union[dict, list]:
        """Returns RPC schema.

        :returns: A list of all supported JSON-RPC endpoints.

        """
        return api.get_rpc_endpoints(self.connection_info)


    def get_rpc_schema(self) -> dict:
        """Returns RPC schema.

        :returns: Node JSON-RPC API schema.

        """
        return api.get_rpc_schema(self.connection_info)


    def get_state_item(
        self,
        item_key: str,
        item_path: typing.Union[str, typing.List[str]] = [],
        state_root_hash: typing.Union[bytes, None] = None
        ) -> bytes:
        """Returns a representation of an item stored under a key in global state.

        :param item_key: Storage item key.
        :param item_path: Storage item path.
        :param state_root_hash: A node's root state hash at some point in chain time, if none then defaults to the most recent.
        :returns: Item stored under passed key/path.

        """
        item_path = item_path if isinstance(item_path, list) else [item_path]
        state_root_hash = state_root_hash or self.get_state_root_hash()
        
        return api.get_state_item(self.connection_info, item_key, item_path, state_root_hash)


    def get_state_root_hash(self, block_id: types.OptionalBlockIdentifer = None) -> bytes:
        """Returns an root hash of global state at a specified block.

        :param block_id: Identifier of a finalised block.
        :returns: State root hash at specified block.

        """
        return bytes.fromhex(
            api.get_state_root_hash(self.connection_info, block_id)
        )
