import time
from typing import Union

from pycspr import factory
from pycspr.api import CasperApi
from pycspr.api import NodeConnectionInfo

# @TODO: rename BlockIndentifer to BlackIdentifier
from pycspr.types import Deploy
from pycspr.types import BlockIdentifer
from pycspr.types import UnforgeableReference
from pycspr.types import DictionaryIdentifier


class QueriesClient():
    """Exposes a set of functions for interacting  with a node.

    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.

        """
        self._api = CasperApi(connection_info)

    def get_account_balance(self, purse_uref: UnforgeableReference,
                            state_root_hash: bytes = None) -> int:
        """
        Returns account balance at a certain global state root hash.

        :param purse_uref: URef of a purse associated with an on-chain account.
        :param state_root_hash: A node's root state hash at some point in chain
                                time, if none then defaults to the most recent.
        :returns: Account balance if on-chain account is found.
        """
        if isinstance(purse_uref, UnforgeableReference):
            purse_uref = purse_uref.as_string()
        if isinstance(state_root_hash, bytes):
            state_root_hash = state_root_hash.hex()
        state_root_hash = state_root_hash or self.get_state_root_hash()
        response = self._api.get_account_balance(purse_uref, state_root_hash)
        return int(response["balance_value"])

    def get_account_info(self, account_key: Union[bytes, str],
                         block_id: BlockIdentifer = None) -> dict:
        """
        Returns account information at a certain global state root hash.

        :param account_key: An account holder's public key prefixed with a key
                            type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.
        """
        account_key = account_key.hex() \
            if isinstance(account_key, bytes) else account_key
        block_id = block_id.hex() if isinstance(block_id, bytes) else block_id

        response = self._api.get_account_info(account_key, block_id)
        return response["account"]

    def get_account_main_purse_uref(self, account_key: Union[bytes, str],
                                    block_id: BlockIdentifer = None
                                    ) -> UnforgeableReference:
        """
        Returns an on-chain account's main purse unforgeable reference.

        :param account_key: Key of an on-chain account.
        :param block_id: Identifier of a finalised block.
        :returns: Account main purse unforgeable reference.
        """
        account_info = self.get_account_info(account_key, block_id)
        return factory.create_uref_from_string(account_info["main_purse"])

    def get_account_named_key(self, account_key: Union[bytes, str],
                              key_name: str,
                              block_id: BlockIdentifer = None) -> str:
        """
        Returns a named key stored under an account.

        :param account_key: An account holder's public key prefixed with a key
                            type identifier.
        :param key_name: Name of key under which account data is stored.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.
        """
        account_info = self._api.get_account_info(account_key, block_id)
        named_keys = [i for i in account_info["named_keys"]
                      if i["name"] == key_name]
        return None if len(named_keys) == 0 else named_keys[0]["key"]

    def get_auction_info(self, block_id: BlockIdentifer = None
                         ) -> dict:
        """
        Returns current auction system contract information.

        :returns: Current auction system contract information.
        """
        block_id = block_id.hex() if isinstance(block_id, bytes) else block_id
        return self._api.get_auction_info(block_id)

    def get_block(self, block_id: BlockIdentifer = None) -> dict:
        """Returns on-chain block information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block information.
        """
        block_id = block_id.hex() if isinstance(block_id, bytes) else block_id
        response = self._api.get_block(block_id)
        return response["block"]

    def get_block_at_era_switch(self, polling_interval_seconds: float = 1.0,
                                max_polling_time_seconds: float = 120.0
                                ) -> dict:
        """
        Returns last finalised block in current era.

        :param polling_interval_seconds: Time interval time (in seconds) before
                                         polling for next switch block.
        :param max_polling_time_seconds: Maximum time in seconds to poll.
        :returns: On-chain block information.
        """
        elapsed = 0.0
        while True:
            block = self.get_block()
            if block["header"]["era_end"] is not None:
                return block
            elapsed += polling_interval_seconds
            if elapsed > max_polling_time_seconds:
                break
            time.sleep(polling_interval_seconds)

    def get_block_transfers(self, block_id: BlockIdentifer = None
                            ) -> tuple[str, list]:
        """
        Returns on-chain block transfers information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block transfers information.
        """
        response = self._api.get_block_transfers(block_id)
        return (response["block_hash"], response["transfers"])

    def get_deploy(self, deploy_id: Union[bytes, str]) -> dict:
        """Returns on-chain deploy information.

        :param deploy_id: Identifier of a finalised block.
        :returns: On-chain deploy information.
        """
        deploy_id = deploy_id.hex() \
            if isinstance(deploy_id, bytes) else deploy_id
        return self._api.get_deploy(deploy_id)

    def get_dictionary_item(self, identifier: DictionaryIdentifier) -> dict:
        """Returns on-chain data stored under a dictionary item.

        :param identifier: Identifier required to query a dictionary item.
        :returns: On-chain data stored under a dictionary item.
        """
        return self._api.get_dictionary_item(identifier.as_api_param())

    def get_era_info(self, block_id: BlockIdentifer = None) -> dict:
        """Returns current era information.

        :param block_id: Identifier of a finalised block.
        :returns: Era information.
        """
        block_id = block_id.hex() if isinstance(block_id, bytes) else block_id
        response = self._api.get_era_info(block_id)
        return response['era_summary']

    def get_node_metrics(self, metric_id: str = None) -> list:
        """Returns set of node metrics.

        :returns: Node metrics information.
        """
        response = self._api.get_node_metrics()
        data = response.content.decode("utf-8")
        data = sorted([i.strip()
                      for i in data.split("\n") if not i.startswith("#")])
        if metric_id:
            return [i for i in data if i.lower().startswith(metric_id.lower())]
        else:
            return data

    def get_node_metric(self, metric_id: str) -> list:
        """Returns node metrics information filtered by a particular metric.

        :param metric_id: Identifier of node metric.
        :returns: Node metrics information filtered by a particular metric.
        """
        return self.get_node_metrics(metric_id)

    def get_node_peers(self) -> dict:
        """Returns node peers information.

        :returns: Node peers information.
        """
        response = self.get_node_status()
        return response['peers']

    def get_node_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.
        """
        return self._api.get_node_status()

    def get_rpc_endpoint(self, endpoint: str) -> dict:
        """Returns RPC schema.

        :param endpoint: A specific endpoint of interest.
        :returns: A JSON-RPC schema endpoint fragment.
        """
        schema = self.get_rpc_schema()
        for obj in schema["methods"]:
            if obj["name"].lower() == endpoint.lower():
                return obj

    def get_rpc_endpoints(self) -> Union[dict, list]:
        """Returns RPC schema.

        :returns: A list of all supported JSON-RPC endpoints.
        """
        schema = self.get_rpc_schema()
        return sorted([i["name"] for i in schema["methods"]])

    def get_rpc_schema(self) -> dict:
        """Returns RPC schema.

        :returns: Node JSON-RPC API schema.
        """
        response = self._api.get_rpc_schema()
        return response["schema"]

    def get_state_item(self, item_key: str,
                       item_path: Union[str, list[str]] = [],
                       state_root_hash: bytes = None) -> bytes:
        """
        Returns a representation of an item stored under a key in global state.

        :param item_key: Storage item key.
        :param item_path: Storage item path.
        :param state_root_hash: A node's root state hash at some point in chain
                                time, if none then defaults to the most recent.
        :returns: Item stored under passed key/path.
        """
        item_path = item_path if isinstance(item_path, list) else [item_path]
        state_root_hash_bytes = state_root_hash or self.get_state_root_hash()
        state_root_hash_str = state_root_hash_bytes.hex()
        response = self._api.get_state_item(item_key, item_path,
                                            state_root_hash_str)
        return response["stored_value"]

    def get_state_root_hash(self, block_id: BlockIdentifer = None
                            ) -> bytes:
        """Returns an root hash of global state at a specified block.

        :param block_id: Identifier of a finalised block.
        :returns: State root hash at specified block.
        """
        block_id = block_id.hex() if isinstance(block_id, bytes) else block_id
        response = self._api.get_state_root_hash(block_id)
        state_root_hash_str = response["state_root_hash"]
        return bytes.fromhex(state_root_hash_str)

    def put_deploy(self, deploy: Deploy) -> dict:
        response = self._api.put_deploy(deploy)
        return response["deploy_hash"]
