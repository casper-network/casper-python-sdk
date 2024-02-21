from pycspr import types
from pycspr.api.connection import NodeConnectionInfo
from pycspr.api.servers import rpc as SERVER


class RpcServerClient():
    """Node RPC server client.

    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.

        :param connection: Information required to connect to a node.

        """
        self.proxy = SERVER.Proxy(
            host=connection_info.host,
            port=connection_info.port_rpc
        )

    def chain_get_block(self, block_id: types.BlockID = None) -> dict:
        """Returns on-chain block information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block information.

        """
        return SERVER.chain_get_block(self.proxy, block_id)

    def chain_get_block_transfers(self, block_id: types.BlockID = None) -> dict:
        """Returns on-chain block transfers information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block transfers information.

        """
        return SERVER.chain_get_block_transfers(self.proxy, block_id)

    def chain_get_era_info_by_switch_block(self, block_id: types.BlockID = None) -> dict:
        """Returns consensus era information scoped by block id.

        :param block_id: Identifier of a block.
        :returns: Era information.

        """
        return SERVER.chain_get_era_info_by_switch_block(self.proxy, block_id)

    def discover(self) -> dict:
        """Returns RPC schema.

        :returns: Node JSON-RPC API schema.

        """
        return SERVER.discover(self.proxy)

    def chain_get_state_root_hash(self, block_id: types.BlockID = None) -> types.StateRootHash:
        """Returns an root hash of global state at a specified block.

        :param block_id: Identifier of a finalised block.
        :returns: State root hash at specified block.

        """
        return SERVER.chain_get_state_root_hash(self.proxy, block_id)

    def info_get_chainspec(self) -> dict:
        """Returns canonical network state information.

        :returns: Chain spec, genesis accounts and global state information.

        """
        return SERVER.info_get_chainspec(self.proxy)

    def info_get_deploy(self, deploy_id: types.DeployID) -> dict:
        """Returns on-chain deploy information.

        :param deploy_id: Identifier of a deploy processed by network.
        :returns: On-chain deploy information.

        """
        return SERVER.info_get_deploy(self.proxy, deploy_id)

    def info_get_peers(self) -> dict:
        """Returns node peer information.

        :returns: Node peer information.

        """
        return SERVER.info_get_peers(self.proxy)

    def info_get_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.

        """
        return SERVER.info_get_status(self.proxy)

    def info_get_validator_changes(self) -> dict:
        """Returns status changes of active validators.

        :param node: Information required to connect to a node.
        :returns: Status changes of active validators.

        """
        return SERVER.info_get_validator_changes(self.proxy)

    def state_get_account_info(self, account_id: types.AccountID, block_id: types.BlockID = None) -> dict:
        """Returns account information at a certain global state root hash.

        :param account_id: An account holder's public key prefixed with a key type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.

        """    
        return SERVER.state_get_account_info(self.proxy, account_id, block_id)    

    def state_get_auction_info(self, block_id: types.BlockID = None) -> dict:
        """Returns current auction system contract information.

        :param block_id: Identifier of a finalised block.
        :returns: Current auction system contract information.

        """
        return SERVER.state_get_auction_info(self.proxy, block_id)

    def query_balance(
        self,
        purse_id: types.PurseID,
        global_state_id: types.GlobalStateID = None
    ) -> int:
        """Returns account balance at a certain point in global state history.

        :param purse_id: Identifier of purse being queried.
        :param global_state_id: Identifier of global state root at some point in time.
        :returns: Account balance in motes (if purse exists).

        """
        return SERVER.query_balance(self.proxy, purse_id, global_state_id)
