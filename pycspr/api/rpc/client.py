import time
import typing

from pycspr.api.rpc.connection import ConnectionInfo
from pycspr.api.rpc.proxy import Proxy
from pycspr.serializer.json.node_rpc import decoder
from pycspr.types.cl import CLV_Key
from pycspr.types.crypto import Digest
from pycspr.types.node.rpc import Address
from pycspr.types.node.rpc import AccountInfo
from pycspr.types.node.rpc import AuctionState
from pycspr.types.node.rpc import Block
from pycspr.types.node.rpc import BlockID
from pycspr.types.node.rpc import BlockTransfers
from pycspr.types.node.rpc import Deploy
from pycspr.types.node.rpc import DeployHash
from pycspr.types.node.rpc import DictionaryID
from pycspr.types.node.rpc import EraSummary
from pycspr.types.node.rpc import GlobalStateID
from pycspr.types.node.rpc import NodePeer
from pycspr.types.node.rpc import NodeStatus
from pycspr.types.node.rpc import PurseID
from pycspr.types.node.rpc import StateRootHash
from pycspr.types.node.rpc import ValidatorChanges
from pycspr.types.node.rpc import URef
from pycspr.utils import convertor


class Client():
    """Node RPC server client.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.proxy = Proxy(connection_info)

        # Alias methods.
        self.get_auction_state = self.get_auction_info
        self.get_era_info = self.get_era_info_by_switch_block
        self.get_state_root_hash = self.get_state_root_hash
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

    async def account_put_deploy(self, deploy: Deploy) -> DeployHash:
        """Dispatches a deploy to a node for processing.

        :param deploy: A deploy to be processed at a node.
        :returns: Deploy hash.

        """
        return await self.proxy.account_put_deploy(deploy)

    async def get_account_balance(
        self,
        purse_id: PurseID,
        global_state_id: GlobalStateID = None
    ) -> int:
        """Returns account balance at a certain point in global state history.

        :param purse_id: Identifier of purse being queried.
        :param global_state_id: Identifier of global state root at some point in time.
        :returns: Account balance in motes (if purse exists).

        """
        return await self.proxy.query_balance(purse_id, global_state_id)

    async def get_account_info(
        self,
        account_id: Address,
        block_id: BlockID = None,
        decode: bool = True
    ) -> typing.Union[dict, AccountInfo]:
        """Returns account information at a certain global state root hash.

        :param account_id: An account holder's public key prefixed with a key type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.

        """
        encoded: dict = await self.proxy.state_get_account_info(account_id, block_id)

        return encoded if decode is False else decoder.decode(encoded, AccountInfo)

    async def get_auction_info(
        self,
        block_id: BlockID = None,
        decode: bool = True
    ) -> typing.Union[dict, AuctionState]:
        """Returns current auction system contract information.

        :param block_id: Identifier of a finalised block.
        :returns: Current auction system contract information.

        """
        encoded: dict = await self.proxy.state_get_auction_info(block_id)

        return encoded if decode is False else decoder.decode(encoded, AuctionState)

    async def get_block(
        self,
        block_id: BlockID = None,
        decode: bool = True
    ) -> typing.Union[dict, Block]:
        """Returns on-chain block information.

        :param block_id: Identifier of a finalised block.
        :param decode: Flag indicating whether to decode API response.
        :returns: On-chain block information.

        """
        encoded: dict = await self.proxy.chain_get_block(block_id)

        return encoded if decode is False else decoder.decode(encoded, Block)

    async def get_block_transfers(
        self,
        block_id: BlockID = None,
        decode: bool = True
    ) -> typing.Union[dict, BlockTransfers]:
        """Returns on-chain block transfers information.

        :param block_id: Identifier of a finalised block.
        :param decode: Flag indicating whether to decode API response.
        :returns: On-chain block transfers information.

        """
        encoded: dict = await self.proxy.chain_get_block_transfers(block_id)

        return encoded if decode is False else decoder.decode(encoded, BlockTransfers)

    async def get_chainspec(self) -> dict:
        """Returns canonical network state information.

        :returns: Chain spec, genesis accounts and global state information.

        """
        return await self.proxy.info_get_chainspec()

    async def get_deploy(
        self,
        deploy_hash: DeployHash,
        decode: bool = True
    ) -> typing.Union[dict, Deploy]:
        """Returns on-chain deploy information.

        :param deploy_id: Hash of a deploy processed by network.
        :param decode: Flag indicating whether to decode API response.
        :returns: On-chain deploy information.

        """
        encoded: dict = await self.proxy.info_get_deploy(deploy_hash)
        encoded["deploy"]["execution_info"] = encoded.get("execution_results", None)

        return \
            encoded["deploy"] if decode is False else \
            decoder.decode(encoded["deploy"], Deploy)

    async def get_dictionary_item(
        self,
        identifier: DictionaryID,
        state_root_hash: StateRootHash = None
    ) -> dict:
        """Returns current auction system contract information.

        :param identifier: Identifier required to query a dictionary item.
        :param state_root_hash: A node's root state hash at some point in chain time.
        :returns: On-chain data stored under a dictionary item.

        """
        # TODO: decode
        return await self.proxy.state_get_dictionary_item(identifier, state_root_hash)

    async def get_era_summary(
        self,
        block_id: BlockID = None,
        decode: bool = True
    ) -> typing.Union[dict, EraSummary]:
        """Returns consensus era summary information.

        :param block_id: Identifier of a block.
        :param decode: Flag indicating whether to decode API response.
        :returns: Era summary information.

        """
        encoded: dict = await self.proxy.chain_get_era_summary(block_id)

        return encoded if decode is False else decoder.decode(encoded, EraSummary)

    async def get_era_info_by_switch_block(
        self,
        block_id: BlockID = None,
        decode: bool = True
    ) -> typing.Union[dict, EraSummary]:
        """Returns consensus era information scoped by block id.

        :param block_id: Identifier of a block.
        :param decode: Flag indicating whether to decode API response.
        :returns: Era information.

        """
        encoded: dict = await self.proxy.chain_get_era_info_by_switch_block(block_id)

        return encoded if decode is False else decoder.decode(encoded, EraSummary)

    async def get_node_peers(
        self,
        decode: bool = True
    ) -> typing.Union[typing.List[dict], typing.List[NodePeer]]:
        """Returns node peer information.

        :param decode: Flag indicating whether to decode API response.
        :returns: Node peer information.

        """
        encoded: list = await self.proxy.info_get_peers()

        return encoded if decode is False else [decoder.decode(i, NodePeer) for i in encoded]

    async def get_node_status(self, decode: bool = True) -> typing.Union[dict, NodeStatus]:
        """Returns node status information.

        :param decode: Flag indicating whether to decode API response.
        :returns: Node status information.

        """
        encoded: dict = await self.proxy.info_get_status()

        return encoded if decode is False else decoder.decode(encoded, NodeStatus)

    async def get_rpc_schema(self) -> dict:
        """Returns RPC schema.

        :returns: Node JSON-RPC API schema.

        """
        return await self.proxy.discover()

    async def get_state_item(
        self,
        key: str,
        path: typing.Union[str, typing.List[str]] = [],
        state_root_hash: StateRootHash = None
    ) -> bytes:
        """Returns a representation of an item stored under a key in global state.

        :param key: Storage item key.
        :param path: Storage item path.
        :param state_root_hash: A node's root state hash at some point in chain time.
        :returns: Item stored under passed key/path.

        """
        # TODO: decode
        return await self.proxy.state_get_item(key, path, state_root_hash)

    async def get_state_key_value(
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
        return await self.proxy.query_global_state(key, path, state_id)

    async def get_state_root_hash(self, block_id: BlockID = None) -> StateRootHash:
        """Returns an root hash of global state at a specified block.

        :param block_id: Identifier of a finalised block.
        :returns: State root hash at specified block.

        """
        return await self.proxy.chain_get_state_root_hash(block_id)

    async def get_state_trie(self, trie_key: Digest) -> typing.Optional[bytes]:
        """Returns results of a query to global state trie store at a specified key.

        :param trie_key: Key of an item stored within global state.
        :returns:  A list of keys read under the specified prefix.

        """
        return await self.proxy.state_get_trie(trie_key)

    async def get_validator_changes(
        self,
        decode: bool = True
    ) -> typing.List[typing.Union[dict, ValidatorChanges]]:
        """Returns status changes of active validators.

        :param node: Information required to connect to a node.
        :returns: Status changes of active validators.

        """
        obj = await self.proxy.info_get_validator_changes()

        return obj if decode is False else [decoder.decode(i, ValidatorChanges) for i in obj]


class ClientExtensions():
    """Node RPC server client extensions, i.e. 2nd order functions.

    """
    def __init__(self, client: Client):
        """Instance constructor.

        :param client: Node RPC client.

        """
        self.client = client

    async def get_account_main_purse_uref(
        self,
        account_id: Address,
        block_id: BlockID = None
    ) -> URef:
        """Returns an on-chain account's main purse unforgeable reference.

        :param account_id: An account holder's public key prefixed with a key type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account main purse unforgeable reference.

        """
        account_info: AccountInfo = await self.client.get_account_info(account_id, block_id)

        return account_info.main_purse

    async def get_account_named_key(
        self,
        account_id: Address,
        key_name: str,
        block_id: BlockID = None
    ) -> CLV_Key:
        """Returns a key stored under an account's storage under a specific name.

        :param account_id: An account holder's public key prefixed with a key type identifier.
        :param key_name: Name of key under which account data is stored.
        :param block_id: Identifier of a finalised block.
        :returns: A CL key if found.

        """
        account_info: AccountInfo = await self.client.get_account_info(account_id, block_id)
        for named_key in account_info.named_keys:
            if named_key.name == key_name:
                return convertor.clv_key_from_str(named_key.key)

    async def get_block_at_era_switch(
        self,
        polling_interval_seconds: float = 1.0,
        max_polling_time_seconds: float = 120.0
    ) -> Block:
        """Returns next switch block.

        :param polling_interval_seconds: Time interval time before polling for next switch block.
        :param max_polling_time_seconds: Maximum time in seconds to poll.
        :returns: On-chain block information.

        """
        elapsed = 0.0
        while True:
            block: Block = await self.client.get_block()
            if block.header.era_end is not None:
                return block

            elapsed += polling_interval_seconds
            if elapsed > max_polling_time_seconds:
                break
            time.sleep(polling_interval_seconds)

    async def get_block_height(self) -> int:
        """Returns height of current block.

        :returns: Hieght of current block.

        """
        _, block_height = await self.get_chain_heights()

        return block_height

    async def get_chain_heights(self) -> typing.Tuple[int, int]:
        """Returns height of current era & block.

        :returns: 2-ary tuple: (era height, block height).

        """
        block: Block = await self.client.get_block(decode=True)

        return block.header.era_id, block.header.height

    async def get_era_height(self) -> int:
        """Returns height of current era.

        :returns: Hieght of current era.

        """
        era_height, _ = await self.get_chain_heights()

        return era_height

    async def get_rpc_endpoint(self, endpoint: str) -> dict:
        """Returns RPC schema.

        :param endpoint: A specific endpoint of interest.
        :returns: A JSON-RPC schema endpoint fragment.

        """
        schema = await self.client.get_rpc_schema()
        for obj in schema["methods"]:
            if obj["name"].lower() == endpoint.lower():
                return obj

    async def get_rpc_endpoints(self) -> typing.Union[dict, list]:
        """Returns RPC schema.

        :returns: A list of all supported JSON-RPC endpoints.

        """
        schema = await self.client.get_rpc_schema()

        return sorted([i["name"] for i in schema["methods"]])
