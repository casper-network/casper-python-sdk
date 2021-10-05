import dataclasses
from typing import Union, List

import requests
import jsonrpcclient

# @TODO: remove Deploy
# pycspr.types should be used only in client and above
from pycspr.types import Deploy
from pycspr.api.constants import RPC_STATE_GET_BALANCE
from pycspr.api.constants import RPC_STATE_GET_ACCOUNT_INFO
from pycspr.api.constants import RPC_STATE_GET_AUCTION_INFO
from pycspr.api.constants import RPC_CHAIN_GET_BLOCK
from pycspr.api.constants import RPC_CHAIN_GET_BLOCK_TRANSFERS
from pycspr.api.constants import RPC_INFO_GET_DEPLOY
from pycspr.api.constants import RPC_CHAIN_GET_ERA_INFO_BY_SWITCH_BLOCK
from pycspr.api.constants import REST_GET_METRICS
from pycspr.api.constants import RPC_INFO_GET_STATUS
from pycspr.api.constants import RPC_DISCOVER
from pycspr.api.constants import RPC_STATE_GET_ITEM
from pycspr.api.constants import RPC_CHAIN_GET_STATE_ROOT_HASH
from pycspr.api.constants import RPC_STATE_GET_DICTIONARY_ITEM
from pycspr.api.constants import RPC_ACCOUNT_PUT_DEPLOY
from pycspr.serialisation.json.encoder.deploy import encode_deploy


__all__ = ["CasperApi", "NodeConnectionInfo", "NodeAPIError"]


class NodeAPIError(Exception):
    def __init__(self, msg):
        super(NodeAPIError, self).__init__(msg)


@dataclasses.dataclass
class NodeConnectionInfo:
    """Encapsulates information required to connect to a node.

    """
    # Node Adress
    host: str = "localhost"
    # ports for rpcs, rest and sse
    port_rest: int = 8888
    port_rpc: int = 7777
    port_sse: int = 9999

    @property
    def address(self) -> str:
        """A node's server base address."""
        return f"http://{self.host}"

    @property
    def address_rest(self) -> str:
        """A node's REST server base address."""
        return f"{self.address}:{self.port_rest}"

    @property
    def address_rpc(self) -> str:
        """A node's RPC server base address."""
        return f"{self.address}:{self.port_rpc}/rpc"

    @property
    def address_sse(self) -> str:
        """A node's SSE server base address."""
        return f"{self.address}:{self.port_sse}/events"

    def __str__(self):
        """Instance string representation."""
        return self.host

    def get_response(self, endpoint: str, params: dict = None) -> dict:
        """Invokes remote JSON-RPC API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :params: Endpoints parameters.
        :returns: Parsed JSON-RPC response.
        """
        response = requests.post(self.address_rpc,
                                 json=jsonrpcclient.request(endpoint,
                                                            params))
        response = jsonrpcclient.parse(response.json())
        if isinstance(response, jsonrpcclient.responses.Error):
            raise NodeAPIError(response)
        else:
            return response.result


class CasperApi:

    def __init__(self, node: NodeConnectionInfo):
        self._node = node

    def get_account_balance(self, purse_uref: str, state_root_hash: str
                            ) -> dict:
        """
        Returns account balance at a certain state root hash.

        :param node: Encapsulates interaction with a remote node.
        :param purse_uref: URef of a purse associated with an on-chain account.
        :param state_root_hash: A node's root state hash at some point in
                                chain time.
        :returns: Account balance if on-chain account is found.
        """
        params = {
            "purse_uref": purse_uref,
            "state_root_hash": state_root_hash
        }
        return self._make_rpc_call(RPC_STATE_GET_BALANCE, params)

    def get_account_info(self, account_key: str,
                         block_id: Union[str, int] = None) -> dict:
        """
        Returns on-chain account information at a certain state root hash.

        :param node: Information required to connect to a node.
        :param account_key: An account holder's public key prefixed with a key
                            type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.
        """
        params = {"public_key": account_key}
        if isinstance(block_id, str):
            params.update({"block_identifier": {"Hash": block_id}})
        elif isinstance(block_id, int):
            params.update({"block_identifier": {"Height": block_id}})

        return self._make_rpc_call(RPC_STATE_GET_ACCOUNT_INFO, params)

    def get_auction_info(self, block_id: Union[str, int] = None) -> dict:
        """
        Returns current auction system contract information.

        :param node: Information required to connect to a node.
        :param block_id: Identifier of a finalised block.
        :returns: Current auction system contract information.
        """
        params = {}
        if isinstance(block_id, str):
            params.update({"block_identifier": {"Hash": block_id}})
        elif isinstance(block_id, int):
            params.update({"block_identifier": {"Height": block_id}})
        return self._make_rpc_call(RPC_STATE_GET_AUCTION_INFO, params)

    def get_block(self, block_id: Union[str, int] = None) -> dict:

        params = {}
        if isinstance(block_id, str):
            params.update({"block_identifier": {"Hash": block_id}})
        elif isinstance(block_id, int):
            params.update({"block_identifier": {"Height": block_id}})
        return self._make_rpc_call(RPC_CHAIN_GET_BLOCK, params)

    def get_block_transfers(self, block_id: Union[str, int] = None) -> dict:
        """
        Returns on-chain block transfers information.

        :param node: Information required to connect to a node.
        :param block_id: Identifier of a finalised block.
        :returns: 2 member tuple of block hash + transfers.
        """
        params = {}
        if isinstance(block_id, str):
            params.update({"block_identifier": {"Hash": block_id}})
        elif isinstance(block_id, int):
            params.update({"block_identifier": {"Height": block_id}})
        return self._make_rpc_call(RPC_CHAIN_GET_BLOCK_TRANSFERS, params)

    def get_deploy(self, deploy_id: str) -> dict:
        """
        Returns on-chain deploy information.

        :param node: Information required to connect to a node.
        :param deploy_id: Identifier of a processed deploy.

        :returns: On-chain deploy information.
        """
        params = {"deploy_hash": deploy_id}
        return self._make_rpc_call(RPC_INFO_GET_DEPLOY, params)

    def get_dictionary_item(self, dict_identifier: dict) -> dict:
        """
        Returns on-chain data stored under a dictionary item.

        :param node: Information required to connect to a node.
        :param identifier: Identifier required to query a dictionary item.
        :returns: On-chain data stored under a dictionary item.
        """
        params = dict_identifier
        return self._make_rpc_call(RPC_STATE_GET_DICTIONARY_ITEM, params)

    def get_era_info(self, block_id: Union[str, int] = None) -> dict:
        params = {}
        if isinstance(block_id, str):
            params.update({"block_identifier": {"Hash": block_id}})
        elif isinstance(block_id, int):
            params.update({"block_identifier": {"Height": block_id}})
        return self._make_rpc_call(RPC_CHAIN_GET_ERA_INFO_BY_SWITCH_BLOCK,
                                   params)

    def get_node_metrics(self):
        return self._make_rest_call(REST_GET_METRICS, {})

    def get_node_status(self):
        """Returns node status information.

        :param node: Information required to connect to a node.
        :returns: Node status information.
        """
        return self._make_rpc_call(RPC_INFO_GET_STATUS, {})

    def get_rpc_schema(self):
        """ Returns RPC schema. """
        return self._make_rpc_call(RPC_DISCOVER, {})

    def get_state_item(self, item_key: str,
                       item_path: Union[str, List[str]] = [],
                       state_root_hash: str = None) -> dict:
        """
        Returns result of a chain query a certain state root hash.

        :param node: Information required to connect to a node.
        :param item_key: A global state storage item key.
        :param item_path: Path(s) to a data held beneath the key.
        :param state_root_hash: A node's root state hash at some point in
                                chain time.
        :returns: Query result in JSON format.
        """
        params = {
                "key": item_key,
                "path": item_path
                if isinstance(item_path, list) else [item_path],
                "state_root_hash": state_root_hash
        }
        return self._make_rpc_call(RPC_STATE_GET_ITEM, params)

    def get_state_root_hash(self, block_id: Union[str, int]):
        """
        Returns an on-chain state root hash at specified block.

        :param node: Information required to connect to a node.
        :param block_id: Identifier of a finalised block.
        :returns: State root hash at specified block.
        """
        params = {}
        if isinstance(block_id, str):
            params.update({"block_identifier": {"Hash": block_id}})
        elif isinstance(block_id, int):
            params.update({"block_identifier": {"Height": block_id}})
        return self._make_rpc_call(RPC_CHAIN_GET_STATE_ROOT_HASH, params)

    def put_deploy(self, deploy: Deploy):
        """Dispatches a deploy to a node for processing.

        :param node: Information required to connect to a node.
        :param deploy: A deploy to be dispatched to a node.
        :returns: Hash of dispatched deploy.
        """
        # @TODO: replace Deploy with a native type,
        #        !!! only use native types in this layer/module
        #        (decoupling...)
        params = {"deploy": encode_deploy(deploy)}
        return self._make_rpc_call(RPC_ACCOUNT_PUT_DEPLOY, params)

    def _make_rpc_call(self, endpoint_name, params):
        response = self._node.get_response(endpoint_name, params)
        return response

    def _make_rest_call(self, endpoint_name, params):
        full_endpoint = (f"{self._node.address_rest}/"
                         f"{endpoint_name}")
        response = requests.get(full_endpoint, params)
        return response

