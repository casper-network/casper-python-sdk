import typing

import jsonrpcclient
import requests

from pycspr import serializer
from pycspr.api import constants
from pycspr.api.rpc import params as param_utils
from pycspr.api.rpc.connection import ConnectionInfo
from pycspr.types.crypto import Digest
from pycspr.types.node.rpc import Deploy
from pycspr.types.node.rpc import Address
from pycspr.types.node.rpc import BlockID
from pycspr.types.node.rpc import DeployHash
from pycspr.types.node.rpc import DictionaryID
from pycspr.types.node.rpc import GlobalStateID
from pycspr.types.node.rpc import GlobalStateIDType
from pycspr.types.node.rpc import PurseID
from pycspr.types.node.rpc import StateRootHash


class Proxy:
    """Node JSON-RPC server proxy.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.connection_info = connection_info

    @property
    def address(self) -> str:
        """A node's RPC server base address."""
        return f"http://{self.connection_info.host}:{self.connection_info.port}/rpc"

    def __str__(self):
        """Instance string representation."""
        return self.address

    async def account_put_deploy(self, deploy: Deploy) -> DeployHash:
        """Dispatches a deploy to a node for processing.

        :param deploy: A deploy to be processed at a node.
        :returns: Deploy hash.

        """
        params: dict = {
            "deploy": serializer.to_json(deploy),
        }

        return await get_response(
            self.address,
            constants.RPC_ACCOUNT_PUT_DEPLOY,
            params,
            "deploy_hash"
            )

    async def chain_get_block(self, block_id: BlockID = None) -> dict:
        """Returns on-chain block information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block information.

        """
        params: dict = param_utils.block_id(block_id, False)

        return await get_response(self.address, constants.RPC_CHAIN_GET_BLOCK, params, "block")

    async def chain_get_block_transfers(self, block_id: BlockID = None) -> dict:
        """Returns on-chain block transfers information.

        :param block_id: Identifier of a finalised block.
        :param decode: Flag indicating whether to decode API response.
        :returns: On-chain block transfers information.

        """
        params: dict = param_utils.block_id(block_id, False)

        return await get_response(self.address, constants.RPC_CHAIN_GET_BLOCK_TRANSFERS, params)

    async def chain_get_era_info_by_switch_block(self, block_id: BlockID = None) -> dict:
        """Returns consensus era information scoped by block id.

        :param block_id: Identifier of a block.
        :returns: Era information.

        """
        params: dict = param_utils.block_id(block_id, False)

        return await get_response(
            self.address,
            constants.RPC_CHAIN_GET_ERA_INFO_BY_SWITCH_BLOCK,
            params,
            "era_summary"
            )

    async def chain_get_era_summary(self, block_id: BlockID = None) -> dict:
        """Returns consensus era summary information.

        :param block_id: Identifier of a block.
        :returns: Era summary information.

        """
        params: dict = param_utils.block_id(block_id, False)

        return await get_response(
            self.address,
            constants.RPC_CHAIN_GET_ERA_SUMMARY,
            params,
            "era_summary"
            )

    async def chain_get_state_root_hash(self, block_id: BlockID = None) -> StateRootHash:
        """Returns root hash of global state at a finalised block.

        :param block_id: Identifier of a finalised block.
        :returns: State root hash at finalised block.

        """
        params: dict = param_utils.block_id(block_id, False)
        response: str = \
            await get_response(
                self.address,
                constants.RPC_CHAIN_GET_STATE_ROOT_HASH,
                params,
                "state_root_hash"
                )

        return bytes.fromhex(response)

    async def discover(self) -> dict:
        """Returns RPC schema.

        :returns: Node JSON-RPC API schema.

        """
        return await get_response(self.address, constants.RPC_DISCOVER, field="schema")

    async def info_get_chainspec(self) -> dict:
        """Returns canonical network state information.

        :returns: Chain spec, genesis accounts and global state information.

        """
        return await get_response(
            self.address,
            constants.RPC_INFO_GET_CHAINSPEC,
            field="chainspec_bytes"
            )

    async def info_get_deploy(
        self,
        deploy_hash: DeployHash,
        finalized_approvals: bool = False
    ) -> dict:
        """Returns on-chain deploy information.

        :param deploy_hash: Hash of a deploy processed by network.
        :returns: On-chain deploy information.

        """
        params: dict = param_utils.deploy_hash(deploy_hash) | {
            "finalized_approvals": finalized_approvals
        }

        return await get_response(self.address, constants.RPC_INFO_GET_DEPLOY, params)

    async def info_get_peers(self) -> typing.List[dict]:
        """Returns node peer information.

        :returns: Node peer information.

        """
        return await get_response(self.address, constants.RPC_INFO_GET_PEERS, field="peers")

    async def info_get_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.

        """
        return await get_response(self.address, constants.RPC_INFO_GET_STATUS)

    async def info_get_validator_changes(self) -> typing.List[dict]:
        """Returns validator change set.

        :returns: Validator change set.

        """
        return await get_response(
            self.address,
            constants.RPC_INFO_GET_VALIDATOR_CHANGES,
            field="changes"
            )

    async def query_balance(
        self,
        purse_id: PurseID,
        global_state_id: GlobalStateID = None
    ) -> int:
        """Returns account balance at a certain point in global state history.

        :param proxy: Remote RPC server proxy.
        :param purse_id: Identifier of purse being queried.
        :param global_state_id: Identifier of global state root at some point in time.
        :returns: Account balance in motes (if purse exists).

        """
        if global_state_id is None:
            global_state_id = GlobalStateID(
                await self.chain_get_state_root_hash(),
                GlobalStateIDType.STATE_ROOT_HASH
            )

        params: dict = \
            param_utils.global_state_id(global_state_id) | \
            param_utils.purse_id(purse_id)
        
        print(params)

        return int(
            await get_response(self.address, constants.RPC_QUERY_BALANCE, params, "balance")
        )

    async def query_global_state(
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
        if state_id is None:
            state_id: GlobalStateID = GlobalStateID(
                await self.chain_get_state_root_hash(),
                GlobalStateIDType.STATE_ROOT_HASH
                )

        params: dict = param_utils.for_query_global_state(key, path, state_id)

        return await get_response(self.address, constants.RPC_QUERY_GLOBAL_STATE, params)

    async def state_get_account_info(
        self,
        account_id: Address,
        block_id: BlockID = None
    ) -> dict:
        """Returns account information at a certain global state root hash.

        :param account_id: An account holder's public key prefixed with a key type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.

        """
        params: dict = \
            param_utils.account_key(account_id) | \
            param_utils.block_id(block_id)

        return await get_response(
            self.address,
            constants.RPC_STATE_GET_ACCOUNT_INFO,
            params,
            "account"
            )

    async def state_get_auction_info(self, block_id: BlockID = None) -> dict:
        """Returns current auction system contract information.

        :param block_id: Identifier of a finalised block.
        :returns: Current auction system contract information.

        """
        params: dict = param_utils.block_id(block_id, False)

        return await get_response(
            self.address,
            constants.RPC_STATE_GET_AUCTION_INFO,
            params,
            "auction_state"
            )

    async def state_get_dictionary_item(
        self,
        identifier: DictionaryID,
        state_root_hash: StateRootHash = None
    ) -> dict:
        """Returns on-chain data stored under a dictionary item.

        :param identifier: Identifier required to query a dictionary item.
        :param state_root_hash: A node's root state hash at some point in chain time.
        :returns: On-chain data stored under a dictionary item.

        """
        if state_root_hash is None:
            state_root_hash = await self.chain_get_state_root_hash()

        params: dict = \
            param_utils.for_state_get_dictionary_item(identifier, state_root_hash)

        return await get_response(self.address, constants.RPC_STATE_GET_DICTIONARY_ITEM, params)

    async def state_get_item(
        self,
        key: str,
        path: typing.Union[str, typing.List[str]] = [],
        state_root_hash: StateRootHash = None
    ) -> bytes:
        """Returns results of a query to global state at a specified block or state root hash.

        :param proxy: Remote RPC server proxy.
        :param key: Key of an item stored within global state.
        :param path: Identifier of a path within item.
        :param state_root_hash: A node's root state hash at some point in chain time.
        :returns: Results of a global state query.

        """
        path = path if isinstance(path, list) else [path]
        state_root_hash = state_root_hash or await self.chain_get_state_root_hash()

        params: dict = param_utils.for_state_get_item(key, path, state_root_hash)

        return await get_response(
            self.address,
            constants.RPC_STATE_GET_ITEM,
            params,
            "stored_value"
            )

    async def state_get_trie(self, trie_key: Digest) -> typing.Optional[bytes]:
        """Returns results of a query to global state trie store at a specified key.

        :param trie_key: Key of an item stored within global state.
        :returns:  A list of keys read under the specified prefix.

        """
        params: dict = {
            "trie_key": trie_key.hex()
        }

        return await get_response(
            self.address,
            constants.RPC_STATE_GET_TRIE, params,
            "maybe_trie_bytes"
            )


class ProxyError(Exception):
    """Node API error wrapper.

    """
    def __init__(self, msg):
        """Instance constructor.

        """
        super(ProxyError, self).__init__(msg)


async def get_response(
    address: str,
    endpoint: str,
    params: dict = None,
    field: str = None,
) -> dict:
    """Invokes JSON-RPC API & returns parsed response.

    :address: Host address.
    :endpoint: Endpoint to invoke.
    :params: Endpoint Parameters.
    :field: Inner response field.
    :returns: Parsed JSON-RPC response.

    """
    request = jsonrpcclient.request(endpoint, params)
    response_raw = requests.post(address, json=request)

    response_parsed = jsonrpcclient.parse(response_raw.json())
    if isinstance(response_parsed, jsonrpcclient.responses.Error):
        raise ProxyError(response_parsed)

    if field is None:
        return response_parsed.result
    else:
        return response_parsed.result[field]
