import datetime
import pathlib
import typing

from pycspr import api_v1
from pycspr import factory
from pycspr.types import AccountInfo
from pycspr.types import CLType
from pycspr.types import CLTypeKey
from pycspr.types import Deploy
from pycspr.types import DeployParameters
from pycspr.types import DeployTimeToLive
from pycspr.types import Digest
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutionInfo
from pycspr.types import ExecutionInfo_ModuleBytes
from pycspr.types import NodeConnectionInfo
from pycspr.types import NodeEventType
from pycspr.types import NODE_REST_ENDPOINTS
from pycspr.types import NODE_RPC_ENDPOINTS
from pycspr.types import NODE_SSE_ENDPOINTS
from pycspr.types import PublicKey
from pycspr.utils import constants
from pycspr.utils import io as _io



class _DeployClient():
    """Exposes a set of functions for interacting  with a node.
    
    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.
        
        """
        self.connection_info = connection_info


    def send(self, deploy: Deploy):
        """Dispatches a deploy to a node for processing.

        :param deploy: A deploy to be processed at a node.

        """
        return api_v1.post_deploy(self.connection_info, deploy)


    def read(self, fpath: typing.Union[pathlib.Path, str]) -> Deploy:
        """Returns a deploy deserialized from file system.

        :fpath: Path to target file.
        :returns: A deploy for dispatch.
        
        """
        return _io.read_deploy(fpath)


    def write(self, deploy: Deploy, fpath: typing.Union[pathlib.Path, str], force: bool = True):
        """Writes a deploy to file system.

        :param deploy: Deploy to be written in JSON format.
        :param fpath: Path to target file.
        :param force: Flag indicating whether deploy will be written if a file already exists.
        
        """
        _io.write_deploy(deploy, fpath, force)


    def create(params: DeployParameters, payment: ExecutionInfo, session: ExecutionInfo):
        """Returns a deploy for subsequent dispatch to a node.
        
        :param params: Standard parameters used when creating a deploy.
        :param session: Session execution information.
        :param payment: Payment execution information.
        :returns: A deploy for dispatch.

        """
        return factory.create_deploy(params, payment, session)


    def create_execution_arg(name: str, parsed: object, cl_type: typing.Union[CLTypeKey, CLType]) -> ExecutionArgument:
        """Returns an argument associated with deploy execution information (session|payment).
        
        :param name: Name of execution argument.
        :param parsed: A parsed value to be dispatched for execution.
        :param cl_type: Type information used to serialize parsed value.
        :returns: A deploy execution argument.

        """
        return factory.create_execution_arg(name, parsed, cl_type)


    def create_standard_payment(amount: int = constants.STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS) -> ExecutionInfo_ModuleBytes:
        """Returns standard payment execution information.
        
        :param amount: Maximum amount in motes to be used for standard payment.

        """
        return factory.create_standard_payment(amount)


    def create_standard_transfer(
        params: DeployParameters,
        amount: int,
        target: bytes,
        correlation_id: int,
        ) -> Deploy:
        """Returns a non-approved native transfer deploy.

        :param params: Standard parameters used when creating a deploy.
        :param amount: Amount in motes to be transferred.
        :param target: Target account hash.
        :param correlation_id: An identifier used by dispatcher to subsequently correlate the transfer to internal systems.
        :returns: A non-approved native transfer deploy.

        """
        return factory.create_standard_transfer(params, amount, target, correlation_id)


    def create_standard_parameters(
        self,
        account: typing.Union[AccountInfo, PublicKey],
        chain_name: str,
        dependencies: typing.List[Digest] = [],
        gas_price: int = constants.DEFAULT_GAS_PRICE,
        timestamp: datetime.datetime = None,
        ttl: typing.Union[str, DeployTimeToLive] = constants.DEFAULT_DEPLOY_TTL
        ) -> DeployParameters:
        """Returns header information associated with a deploy.
        
        :param account: Account dispatching deploy.
        :param chain_name: Identifier of target chain.
        :param dependencies: Array of hashes of deploys that must be processed prior to this one.
        :param gas_price: Array of hashes of deploys that must be processed prior to this one.
        :param timestamp: Milliseconds since epoch when deploy was instantiated.
        :param ttl: Humanized time interval prior to which deploy must be processed.

        """
        return factory.create_standard_parameters(account, chain_name, dependencies, gas_price, timestamp, ttl)


class _EventsClient():
    """Exposes a set of functions for interacting  with a node's server sent event endpoints.
    
    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.
        
        """
        self.connection_info = connection_info


class _QueryClient():
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
        state_root_hash = state_root_hash or get_state_root_hash()
    
        return api_v1.get_account_balance(self.connection_info, purse_uref, state_root_hash)


    def get_account_info(self, account_hash: bytes, state_root_hash: typing.Union[bytes, None] = None) -> dict:
        """Returns account information at a certain global state root hash.

        :param account_hash: An on-chain account identifier derived from it's associated public key.
        :param state_root_hash: A node's root state hash at some point in chain time, if none then defaults to the most recent.

        :returns: Account information in JSON format.

        """
        state_root_hash = state_root_hash or get_state_root_hash()

        return api_v1.get_account_info(self.connection_info, account_hash, state_root_hash)


    def get_account_main_purse_uref(self, account_key: bytes, state_root_hash: typing.Union[bytes, None] = None) -> str:
        """Returns an on-chain account's main purse unforgeable reference.

        :param account_key: Key of an on-chain account.
        :param state_root_hash: A node's root state hash at some point in chain time, if none then defaults to the most recent.
        :returns: Account main purse unforgeable reference.

        """
        state_root_hash = state_root_hash or get_state_root_hash()

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


    def get_block_at_era_switch(self, polling_interval_seconds: float = 1.0, max_polling_time_seconds: float = 120.0) -> dict:
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


    def get_era_info(block_id: typing.Union[None, bytes, str, int] = None) -> dict:
        """Returns current era information.

        :param block_id: Identifier of a finialised block.
        :returns: Era information.

        """
        return api_v1.get_era_info(self.connection_info, block_id)


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


    def get_state_item(self, item_key: str, item_path: typing.List[str] = [], state_root_hash: typing.Union[bytes, None] = None) -> bytes:
        """Returns a representation of an item stored under a key in global state.

        :param block_id: Identifier of a finialised block.
        :returns: State root hash at specified block.

        """
        state_root_hash = state_root_hash or get_state_root_hash()
        
        return api_v1.get_state_item(self.connection_info, item_key, item_key, state_root_hash)


    def get_state_root_hash(self, block_id: typing.Union[None, str, int] = None) -> bytes:
        """Returns an root hash of global state at a specified block.

        :param block_id: Identifier of a finialised block.
        :returns: State root hash at specified block.

        """
        return bytes.fromhex(
            api_v1.get_state_root_hash(self.connection_info, block_id)
        )


class NodeClient():
    """Exposes a set of functions for interacting  with a node.
    
    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.
        
        """
        self.connection_info = connection_info
        self.deploys = _DeployClient(connection_info)
        self.events = _EventsClient(connection_info)
        self.queries = _QueryClient(connection_info)
        self.NODE_REST_ENDPOINTS = NODE_REST_ENDPOINTS
        self.NODE_RPC_ENDPOINTS = NODE_RPC_ENDPOINTS
        self.NODE_SSE_ENDPOINTS = NODE_SSE_ENDPOINTS
    