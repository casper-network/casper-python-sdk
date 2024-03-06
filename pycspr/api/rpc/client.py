import time
import typing

from pycspr.api.connection import NodeConnectionInfo
from pycspr.api.rpc import decoder
from pycspr.api.rpc.proxy import Proxy
from pycspr.api.rpc import types as rpc_types
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
        self.proxy = Proxy(
            host=connection_info.host,
            port=connection_info.port_rpc,
        )

        # Alias methods.
        self.get_auction_state = self.get_auction_info
        self.get_era_info = self.get_era_info_by_switch_block
        self.get_state_root_hash = self.get_state_root
        self.send_deploy = self.account_put_deploy

        # Extension methods -> 2nd order functions.
        ext = ClientExtensions(self)
        self.get_account_main_purse_uref = ext.get_account_main_purse_uref
        self.get_account_named_key = ext.get_account_named_key
        self.get_block_at_era_switch = ext.get_block_at_era_switch
        self.get_block_height = ext.get_block_height
        self.get_chain_heights = ext.get_chain_heights
        self.get_era_height = ext.get_era_height
        self.get_rpc_endpoint = ext.get_rpc_endpoint
        self.get_rpc_endpoints = ext.get_rpc_endpoints

    def account_put_deploy(self, deploy: Deploy) -> DeployID:
        """Dispatches a deploy to a node for processing.

        :param deploy: A deploy to be processed at a node.
        :returns: Deploy identifier.

        """
        return self.proxy.account_put_deploy(deploy)

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
        return self.proxy.query_balance(purse_id, global_state_id)

    def get_account_info(
        self,
        account_id: AccountID,
        block_id: BlockID = None,
        decode=False
    ) -> typing.Union[dict, rpc_types.AccountInfo]:
        """Returns account information at a certain global state root hash.

        :param account_id: An account holder's public key prefixed with a key type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.

        """
        obj: dict = self.proxy.state_get_account_info(account_id, block_id)

        return obj if decode is False else decoder.decode(obj, rpc_types.AccountInfo)

    def get_auction_info(
        self,
        block_id: BlockID = None,
        decode: bool = True
    ) -> typing.Union[dict, rpc_types.AuctionState]:
        """Returns current auction system contract information.

        :param block_id: Identifier of a finalised block.
        :returns: Current auction system contract information.

        """
        obj: dict = self.proxy.state_get_auction_info(block_id)

        return obj if decode is False else decoder.decode(obj, rpc_types.AuctionState)

    def get_block(
        self,
        block_id: BlockID = None,
        decode=False
    ) -> typing.Union[dict, rpc_types.Block]:
        """Returns on-chain block information.

        :param block_id: Identifier of a finalised block.
        :param decode: Flag indicating whether to decode API response.
        :returns: On-chain block information.

        """
        obj: dict = self.proxy.chain_get_block(block_id)

        return obj if decode is False else decoder.decode(obj, rpc_types.Block)

    def get_block_transfers(
        self,
        block_id: BlockID = None,
        decode: bool = True
    ) -> typing.Union[dict, rpc_types.BlockTransfers]:
        """Returns on-chain block transfers information.

        :param block_id: Identifier of a finalised block.
        :param decode: Flag indicating whether to decode API response.
        :returns: On-chain block transfers information.

        """
        obj: dict = self.proxy.chain_get_block_transfers(block_id)

        return obj if decode is False else decoder.decode(obj, rpc_types.BlockTransfers)

    def get_chainspec(self) -> dict:
        """Returns canonical network state information.

        :returns: Chain spec, genesis accounts and global state information.

        """
        # TODO: decode
        return self.proxy.info_get_chainspec()

    def get_deploy(
        self,
        deploy_id: DeployID,
        decode: bool = True
    ) -> typing.Union[dict, rpc_types.Deploy]:
        """Returns on-chain deploy information.

        :param deploy_id: Identifier of a deploy processed by network.
        :param decode: Flag indicating whether to decode API response.
        :returns: On-chain deploy information.

        """
        obj: dict = self.proxy.info_get_deploy(deploy_id)
        obj["deploy"]["execution_info"] = obj.get("execution_results", None)

        return obj["deploy"] if decode is False else decoder.decode(obj["deploy"], rpc_types.Deploy)

    def get_dictionary_item(
        self,
        identifier: DictionaryID,
        state_root_hash: StateRootID = None
    ) -> dict:
        """Returns current auction system contract information.

        :param identifier: Identifier required to query a dictionary item.
        :param state_root_hash: A node's root state hash at some point in chain time.
        :returns: On-chain data stored under a dictionary item.

        """
        # TODO: decode
        return self.proxy.state_get_dictionary_item(identifier, state_root_hash)

    def get_era_summary(
        self,
        block_id: BlockID = None,
        decode: bool = True
    ) -> typing.Union[dict, rpc_types.EraSummary]:
        """Returns consensus era summary information.

        :param block_id: Identifier of a block.
        :returns: Era summary information.

        """
        obj: dict = self.proxy.chain_get_era_summary(block_id)

        return obj if decode is False else decoder.decode(obj, rpc_types.EraSummary)

    def get_era_info_by_switch_block(self, block_id: BlockID = None) -> dict:
        """Returns consensus era information scoped by block id.

        :param block_id: Identifier of a block.
        :returns: Era information.

        """
        # TODO: decode
        return self.proxy.chain_get_era_info_by_switch_block(block_id)

    def get_node_peers(self) -> dict:
        """Returns node peer information.

        :returns: Node peer information.

        """
        # TODO: decode
        return self.proxy.info_get_peers()

    def get_node_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.

        """
        # TODO: decode
        return self.proxy.info_get_status()

    def get_rpc_schema(self) -> dict:
        """Returns RPC schema.

        :returns: Node JSON-RPC API schema.

        """
        # TODO: decode
        return self.proxy.discover()

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
        # TODO: decode
        return self.proxy.state_get_item(key, path, state_root_hash)

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
        # TODO: decode
        return self.proxy.query_global_state(key, path, state_id)

    def get_state_root(self, block_id: BlockID = None) -> StateRootID:
        """Returns an root hash of global state at a specified block.

        :param block_id: Identifier of a finalised block.
        :returns: State root hash at specified block.

        """
        return self.proxy.chain_get_state_root_hash(block_id)

    def get_validator_changes(
        self,
        decode: bool = True
    ) -> typing.List[typing.Union[dict, rpc_types.ValidatorChanges]]:
        """Returns status changes of active validators.

        :param node: Information required to connect to a node.
        :returns: Status changes of active validators.

        """
        obj = self.proxy.info_get_validator_changes()

        return obj if decode is False else [decoder.decode(i, rpc_types.ValidatorChanges) for i in obj]


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
