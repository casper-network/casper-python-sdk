import datetime
import typing

from pycspr import crypto
from pycspr.factory.accounts import create_public_key
from pycspr.factory.cl import create_cl_type_of_byte_array
from pycspr.factory.cl import create_cl_type_of_option
from pycspr.factory.cl import create_cl_type_of_simple
from pycspr.factory.cl import create_cl_value
from pycspr.factory.digests import create_digest_of_deploy
from pycspr.factory.digests import create_digest_of_deploy_body
from pycspr.types import AccountInfo
from pycspr.types import PublicKey
from pycspr.types import CLTypeKey
from pycspr.types import CLType
from pycspr.types import Deploy
from pycspr.types import DeployApproval
from pycspr.types import DeployBody
from pycspr.types import DeployHeader
from pycspr.types import DeployTimeToLive
from pycspr.types import Digest
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutionInfo
from pycspr.types import ExecutionInfo_ModuleBytes
from pycspr.types import ExecutionInfo_Transfer
from pycspr.types import DeployParameters
from pycspr.utils import constants
from pycspr.utils import conversion



def create_deploy(std_params: DeployParameters, payment: ExecutionInfo, session: ExecutionInfo):
    """Returns a deploy for subsequent dispatch to a node.
    
    :param std_params: Standard parameters used when creating a deploy.
    :param session: Session execution information.
    :param payment: Payment execution information.

    """
    body = create_deploy_body(payment, session)
    header = create_deploy_header(body, std_params)

    return Deploy(
        approvals=[],
        hash=create_digest_of_deploy(header),
        header=header,
        payment=payment,
        session=session
    )


def create_deploy_body(payment: ExecutionInfo, session: ExecutionInfo) -> DeployBody:
    """Returns hash of a deploy's so-called body.
    
    :param payment: Payment execution information.
    :param session: Session execution information.

    """
    return DeployBody(
        session,
        payment,
        create_digest_of_deploy_body(payment, session)
        )


def create_deploy_header(body: DeployBody, params: DeployParameters) -> DeployHeader:
    """Returns header information associated with a deploy.
    
    :param body: Deploy body, i.e. it's session/payment execution information.
    :param params: Standard parameters associated with a deploy.

    """
    return DeployHeader(
        accountPublicKey=params.accountPublicKey,
        body_hash=body.hash,
        chain_name=params.chain_name,
        dependencies=params.dependencies,
        gas_price=params.gas_price,
        timestamp=params.timestamp,
        ttl=params.ttl,
    )


def create_deploy_parameters(
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
    public_key = account if isinstance(account, PublicKey) else \
                 create_public_key(account.algo, account.pbk)
    if timestamp is None:
        timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    timestamp = round(timestamp, 3)
    ttl = create_deploy_ttl(ttl) if isinstance(ttl, str) else ttl

    return DeployParameters(
        accountPublicKey=public_key,
        chain_name=chain_name,
        dependencies=dependencies,
        gas_price=gas_price,
        timestamp=timestamp,
        ttl=ttl,
    )


def create_deploy_ttl(humanized_ttl: str = constants.DEFAULT_DEPLOY_TTL) -> DeployTimeToLive:
    """Returns a deploy's time to live after which it will not longer be accepted by a node.
    
    :param humanized_ttl: A humanized ttl, e.g. 1 day.

    """
    as_milliseconds = conversion.humanized_time_interval_to_milliseconds(humanized_ttl)
    if as_milliseconds > constants.DEPLOY_TTL_MS_MAX:
        raise ValueError(f"Invalid deploy ttl {humanized_ttl} = {as_milliseconds} ms.  Maximum (ms) = {constants.DEPLOY_TTL_MS_MAX}")

    return DeployTimeToLive(
        humanized=humanized_ttl,
        as_milliseconds=as_milliseconds
    )


def create_execution_arg(
    name: str,
    parsed: object, 
    cl_type: typing.Union[CLTypeKey, CLType]
    ) -> ExecutionArgument:
    """Returns an argument associated with deploy execution information (session|payment).
    
    :param name: Name of execution argument.
    :param parsed: A parsed value to be dispatched for execution.
    :param cl_type: Type information used to serialize parsed value.

    """
    return ExecutionArgument(
        name=name,
        value=create_cl_value(cl_type, parsed)
    )


def create_standard_payment(
    amount: int = constants.STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS
    ) -> ExecutionInfo_ModuleBytes:
    """Returns standard payment execution information.
    
    :param amount: Maximum amount in motes to be used for standard payment.

    """
    return ExecutionInfo_ModuleBytes(
        args=[
            create_execution_arg(
                "amount",
                amount,
                create_cl_type_of_simple(CLTypeKey.U512)
                ),
        ],
        module_bytes=bytes([])
        )


def create_standard_transfer(
    std_params: DeployParameters,
    amount: int,
    target: bytes,
    correlation_id: int,
    ) -> Deploy:
    """Returns a native transfer deploy.

    :param std_params: Standard parameters used when creating a deploy.
    :param amount: Amount in motes to be transferred.
    :param target: Target account hash.
    :param correlation_id: An identifier used by dispatcher to subsequently correlate the transfer to internal systems.
    :returns: A native transfer deploy.

    """
    return create_deploy(
        std_params,
        create_standard_transfer_session(
            amount,
            target,
            correlation_id
        ),
        create_standard_payment(constants.STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS)
        )


def create_standard_transfer_session(
    amount: int,
    target: bytes,
    correlation_id: int,
    ) -> ExecutionInfo_Transfer:
    """Returns session execution information for a native transfer.

    :param amount: Amount in motes to be transferred.
    :param target: Target account hash.
    :param correlation_id: An identifier used by dispatcher to subsequently correlate the transfer to internal systems.
    
    """
    return ExecutionInfo_Transfer(
        args=[
            create_execution_arg(
                "amount",
                amount,
                create_cl_type_of_simple(CLTypeKey.U512)
                ),
            create_execution_arg(
                "target",
                target,
                create_cl_type_of_byte_array(32)
                ),
            create_execution_arg(
                "id",
                correlation_id,
                create_cl_type_of_option(create_cl_type_of_simple(CLTypeKey.U64))
                ),
        ]
    )
