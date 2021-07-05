import datetime
import typing

from pycspr import crypto
from pycspr import factory
from pycspr.types.account import AccountInfo
from pycspr.types.cl import CLTypeKey
from pycspr.types.cl import CLType
from pycspr.types.deploy import Approval
from pycspr.types.deploy import Deploy
from pycspr.types.deploy import DeployBody
from pycspr.types.deploy import DeployHeader
from pycspr.types.deploy import Digest
from pycspr.types.deploy import ExecutionArgument
from pycspr.types.deploy import ExecutionInfo
from pycspr.types.deploy import ExecutionInfo_ModuleBytes
from pycspr.types.deploy import ExecutionInfo_Transfer
from pycspr.types.deploy import StandardParameters


def create_approval(account: AccountInfo, data: bytes) -> Approval:
    """Returns an approval by an account to the effect of authorizing deploy processing.
    
    :param account: An account authorising upstream deploy processing.
    :param data: Payload to be signed.

    """
    return Approval(
        signer=account.public_key, 
        signature=crypto.get_signature(
            data,
            account.private_key,
            algo=account.algo
            )
        )


def create_body(payment: ExecutionInfo, session: ExecutionInfo) -> DeployBody:
    """Returns hash of a deploy's so-called body.
    
    :param payment: Payment execution information.
    :param session: Session execution information.

    """
    body_hash = factory.digests.get_digest_of_deploy_body(payment, session)

    return DeployBody(session, payment, body_hash)


def create_deploy(params: StandardParameters, payment: ExecutionInfo, session: ExecutionInfo):
    """Returns a deploy for subsequent dispatch to a node.
    
    :param params: Standard parameters used when creating a deploy.
    :param session: Session execution information.
    :param payment: Payment execution information.

    """
    body = create_body(payment, session)
    header = create_header(body, params)
    deploy_hash = factory.digests.get_digest_of_deploy(header)  

    return Deploy(
        approvals=[],
        hash=deploy_hash,
        header=header,
        payment=payment,
        session=session
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
        name = name,
        value = factory.cl.create_value(cl_type, parsed)
    )


def create_header(
    body: DeployBody,
    params: StandardParameters,
    ) -> DeployHeader:
    """Returns header information associated with a deploy.
    
    :param body: Deploy body, i.e. it's session/payment execution information.
    :param params: Standard parameters associated with a deploy.

    """
    timestamp = params.timestamp or datetime.datetime.utcnow().timestamp()

    return DeployHeader(
        account=params.account,
        body_hash=body.hash,
        chain_name=params.chain_name,
        dependencies=params.dependencies,
        gas_price=params.gas_price,
        timestamp=timestamp,
        ttl=params.ttl,
    )


def create_payment_for_transfer(amount: int = 10000) -> ExecutionInfo_ModuleBytes:
    """Returns payment execution information for a native transfer.
    
    :param amount: Maximum amount in motes to be used for payment.

    """
    return ExecutionInfo_ModuleBytes(
        args=[
            create_execution_arg(
                "amount",
                amount,
                factory.cl.create_simple(CLTypeKey.U512)
                ),
        ],
        module_bytes=bytes([])
        )


def create_session_for_transfer(
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
                factory.cl.create_simple(CLTypeKey.U512)
                ),
            create_execution_arg(
                "target",
                target,
                factory.cl.create_byte_array(32)
                ),
            create_execution_arg(
                "id",
                correlation_id,
                factory.cl.create_option(factory.cl.create_simple(CLTypeKey.U64))
                ),
        ]
    )


def create_standard_parameters(
    account: AccountInfo,
    chain_name: str,
    dependencies: typing.List[Digest] = [],
    gas_price: int = 1,
    timestamp: datetime.datetime = None,
    ttl: str = "1day"
    ) -> StandardParameters:
    """Returns header information associated with a deploy.
    
    :param account: Account dispatching deploy.
    :param chain_name: Identifier of target chain.
    :param dependencies: Array of hashes of deploys that must be processed prior to this one.
    :param gas_price: Array of hashes of deploys that must be processed prior to this one.
    :param timestamp: Milliseconds since epoch when deploy was instantiated.
    :param ttl: Humanized time interval prior to which deploy must be processed.

    """
    timestamp = timestamp or datetime.datetime.utcnow().timestamp()

    return StandardParameters(
        account=account.account_key,
        chain_name=chain_name,
        dependencies=dependencies,
        gas_price=gas_price,
        timestamp=timestamp,
        ttl=ttl,
    )
