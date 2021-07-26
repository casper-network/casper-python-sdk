import datetime
import pathlib
import typing

from pycspr import api_v1
from pycspr import factory
from pycspr.client import NodeConnectionInfo
from pycspr.types import PrivateKey
from pycspr.types import CLType
from pycspr.types import CLTypeKey
from pycspr.types import Deploy
from pycspr.types import DeployParameters
from pycspr.types import DeployTimeToLive
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutableDeployItem
from pycspr.types import ExecutableDeployItem_ModuleBytes
from pycspr.types import PublicKey
from pycspr.utils import constants
from pycspr.utils import io as _io



class DeploysClient():
    """Exposes a set of functions for processing deploys.
    
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


    def create(params: DeployParameters, payment: ExecutableDeployItem, session: ExecutableDeployItem):
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


    def create_standard_payment(amount: int = constants.STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS) -> ExecutableDeployItem_ModuleBytes:
        """Returns standard payment execution information.
        
        :param amount: Maximum amount in motes to be used for standard payment.

        """
        return factory.create_standard_payment(amount)


    def create_standard_parameters(
        self,
        account: typing.Union[PrivateKey, PublicKey],
        chain_name: str,
        dependencies: typing.List[bytes] = [],
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


    def create_native_transfer(
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
        return factory.create_native_transfer(params, amount, target, correlation_id)
