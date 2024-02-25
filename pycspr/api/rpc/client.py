import time
import typing

from pycspr.api.connection import NodeConnectionInfo
from pycspr.api.rpc import endpoints
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import AccountID
from pycspr.types import BlockID
from pycspr.types import CL_Key
from pycspr.types import CL_URef
from pycspr.types import DeployID
from pycspr.types import Deploy
from pycspr.types import DictionaryID
from pycspr.types import GlobalStateID
from pycspr.types import PurseID
from pycspr.types import StateRootID


class Client():
    """Node RPC server client.

    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.

        :param connection: Information required to connect to a node.

        """
        self.ext = ClientExtensions(self)
        self.proxy = Proxy(
            host=connection_info.host,
            port=connection_info.port_rpc
        )

    def account_put_deploy(self, deploy: Deploy) -> DeployID:
        """Dispatches a deploy to a node for processing.

        :param deploy: A deploy to be processed at a node.
        :returns: Deploy identifier.

        """
        return endpoints.account_put_deploy(self.proxy, deploy)

    def get_account_balance(
        self,
        purse_id: PurseID,
        global_state_id: GlobalStateID = None
    ) -> int:
        """Returns account balance at a certain point in global state history.

        :param purse_id: Identifier of purse being queried.
        :param global_state_id: Identifier of global state root at some point in time.
        :returns: Account balance in motes (if purse exists).

        """
        return endpoints.query_balance(self.proxy, purse_id, global_state_id)

    def get_account_info(self, account_id: AccountID, block_id: BlockID = None) -> dict:
        """Returns account information at a certain global state root hash.

        :param account_id: An account holder's public key prefixed with a key type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.

        """
        return endpoints.state_get_account_info(self.proxy, account_id, block_id)

    def get_auction_info(self, block_id: BlockID = None) -> dict:
        """Returns current auction system contract information.

        :param block_id: Identifier of a finalised block.
        :returns: Current auction system contract information.

        """
        return endpoints.state_get_auction_info(self.proxy, block_id)

    def get_block(self, block_id: BlockID = None) -> dict:
        """Returns on-chain block information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block information.

        """
        return endpoints.chain_get_block(self.proxy, block_id)

    def get_block_transfers(self, block_id: BlockID = None) -> dict:
        """Returns on-chain block transfers information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block transfers information.

        """
        return endpoints.chain_get_block_transfers(self.proxy, block_id)

    def get_chainspec(self) -> dict:
        """Returns canonical network state information.

        :returns: Chain spec, genesis accounts and global state information.

        """
        return endpoints.info_get_chainspec(self.proxy)

    def get_deploy(self, deploy_id: DeployID) -> dict:
        """Returns on-chain deploy information.

        :param deploy_id: Identifier of a deploy processed by network.
        :returns: On-chain deploy information.

        """
        return endpoints.info_get_deploy(self.proxy, deploy_id)

    def get_dictionary_item(
        self,
        identifier: DictionaryID,
        state_root_hash: StateRootID = None
    ) -> dict:
        """Returns current auction system contract information.

        :param block_id: Identifier of a finalised block.
        :returns: Current auction system contract information.

        """
        return endpoints.state_get_dictionary_item(self.proxy, identifier, state_root_hash)

    def get_era_summary(self, block_id: BlockID = None) -> dict:
        """Returns consensus era summary information.

        :param block_id: Identifier of a block.
        :returns: Era summary information.

        """
        return endpoints.chain_get_era_summary(self.proxy, block_id)

    def get_era_info_by_switch_block(self, block_id: BlockID = None) -> dict:
        """Returns consensus era information scoped by block id.

        :param block_id: Identifier of a block.
        :returns: Era information.

        """
        return endpoints.chain_get_era_info_by_switch_block(self.proxy, block_id)

    def get_node_peers(self) -> dict:
        """Returns node peer information.

        :returns: Node peer information.

        """
        return endpoints.info_get_peers(self.proxy)

    def get_node_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.

        """
        return endpoints.info_get_status(self.proxy)

    def get_rpc_schema(self) -> dict:
        """Returns RPC schema.

        :returns: Node JSON-RPC API schema.

        """
        return endpoints.discover(self.proxy)

    def get_state_item(
        self,
        key: str,
        path: typing.Union[str, typing.List[str]] = [],
        state_root_hash: StateRootID = None
    ) -> bytes:
        """Returns a representation of an item stored under a key in global state.

        :param key: Storage item key.
        :param path: Storage item path.
        :param state_root_hash: A node's root state hash at some point in chain time.
        :returns: Item stored under passed key/path.

        """
        return endpoints.state_get_item(self.proxy, key, path, state_root_hash)

    def get_state_key_value(
        self,
        key: str,
        path: typing.List[str],
        state_id: GlobalStateID = None
    ) -> bytes:
        """Returns results of a query to global state at a specified block or state root hash.

        :param key: Key of an item stored within global state.
        :param path: Identifier of a path within item.
        :param state_id: Identifier of global state leaf.
        :returns: Results of a global state query.

        """
        return endpoints.query_global_state(self.proxy, key, path, state_id)

    def get_state_root(self, block_id: BlockID = None) -> StateRootID:
        """Returns an root hash of global state at a specified block.

        :param block_id: Identifier of a finalised block.
        :returns: State root hash at specified block.

        """
        return endpoints.chain_get_state_root_hash(self.proxy, block_id)

    def get_validator_changes(self) -> dict:
        """Returns status changes of active validators.

        :param node: Information required to connect to a node.
        :returns: Status changes of active validators.

        """
        return endpoints.info_get_validator_changes(self.proxy)


class ClientExtensions():
    """Node RPC server client extensions, i.e. 2nd order functions.

    """
    def __init__(self, client: Client):
        """Instance constructor.

        :param client: Node RPC client.

        """
        self.client = client

    def get_account_main_purse_uref(
        self,
        account_id: AccountID,
        block_id: BlockID = None
    ) -> CL_URef:
        """Returns an on-chain account's main purse unforgeable reference.

        :param account_id: An account holder's public key prefixed with a key type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account main purse unforgeable reference.

        """
        account_info = self.client.get_account_info(account_id, block_id)

        return CL_URef.from_string(account_info["main_purse"])

    def get_account_named_key(
        self,
        account_id: AccountID,
        key_name: str,
        block_id: BlockID = None
    ) -> CL_Key:
        """Returns a key stored under an account's storage under a specific name.

        :param account_id: An account holder's public key prefixed with a key type identifier.
        :param key_name: Name of key under which account data is stored.
        :param block_id: Identifier of a finalised block.
        :returns: A CL key if found.

        """
        account_info = self.client.get_account_info(account_id, block_id)
        for named_key in account_info["named_keys"]:
            if named_key["name"] == key_name:
                return CL_Key.from_string(named_key["key"])

    def get_block_at_era_switch(
        self,
        polling_interval_seconds: float = 1.0,
        max_polling_time_seconds: float = 120.0
    ) -> dict:
        """Returns next switch block.

        :param polling_interval_seconds: Time interval time before polling for next switch block.
        :param max_polling_time_seconds: Maximum time in seconds to poll.
        :returns: On-chain block information.

        """
        elapsed = 0.0
        while True:
            block = self.client.get_block()
            if block["header"]["era_end"] is not None:
                return block

            elapsed += polling_interval_seconds
            if elapsed > max_polling_time_seconds:
                break
            time.sleep(polling_interval_seconds)

    def get_block_height(self) -> int:
        """Returns height of current block.

        :returns: Hieght of current block.

        """
        _, block_height = self.get_chain_heights()

        return block_height

    def get_chain_heights(self) -> int:
        """Returns height of current era & block.

        :returns: 2-ary tuple: (era height, block height).

        """
        block: dict = self.client.get_block()

        return block["header"]["era_id"], block["header"]["height"]

    def get_era_height(self) -> int:
        """Returns height of current era.

        :returns: Hieght of current era.

        """
        era_height, _ = self.get_chain_heights()

        return era_height

    def get_rpc_endpoint(self, endpoint: str) -> dict:
        """Returns RPC schema.

        :param endpoint: A specific endpoint of interest.
        :returns: A JSON-RPC schema endpoint fragment.

        """
        schema = self.client.get_rpc_schema()
        for obj in schema["methods"]:
            if obj["name"].lower() == endpoint.lower():
                return obj

    def get_rpc_endpoints(self) -> typing.Union[dict, list]:
        """Returns RPC schema.

        :returns: A list of all supported JSON-RPC endpoints.

        """
        schema = self.client.get_rpc_schema()

        return sorted([i["name"] for i in schema["methods"]])
