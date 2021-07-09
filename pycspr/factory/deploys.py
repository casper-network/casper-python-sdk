import datetime
import typing

from pycspr import crypto
from pycspr import factory
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


def create_deploy_approval(account: AccountInfo, deploy: Deploy) -> DeployApproval:
    """Returns an approval by an account to the effect of authorizing deploy processing.
    
    :param account: An account authorising upstream deploy processing.
    :param data: Payload to be signed.

    """
    # TODO: push this to deploy dispatcher - i.e. refuse to push to node if approval set is invalid.
    # Reset approval set if deploy hash has changed since last signattures were applied.
    if deploy.approvals:
        deploy_hash_memo = deploy.hash
        deploy.header.body_hash = create_digest_of_deploy_body(deploy.session, deploy.payment)
        deploy.hash = create_digest_of_deploy(deploy.header)
        if deploy.hash != deploy_hash_memo:
            deploy.approvals = []

    # Extend (de-duplicated) approval set.approval set.
    deploy.approvals.append(
        DeployApproval(
            signer=account.account_key, 
            signature=crypto.get_signature(
                bytes.fromhex(deploy.hash),
                account.private_key,
                algo=account.algo,
                encoding=crypto.SignatureEncoding.HEX
                )
            )
        )

    return deploy.approvals[-1]


def create_deploy_body(payment: ExecutionInfo, session: ExecutionInfo) -> DeployBody:
    """Returns hash of a deploy's so-called body.
    
    :param payment: Payment execution information.
    :param session: Session execution information.

    """
    return DeployBody(
        session,
        payment,
        factory.create_digest_of_deploy_body(payment, session)
        )


def create_deploy_header(body: DeployBody, params: DeployParameters) -> DeployHeader:
    """Returns header information associated with a deploy.
    
    :param body: Deploy body, i.e. it's session/payment execution information.
    :param params: Standard parameters associated with a deploy.

    """
    timestamp = params.timestamp or datetime.datetime.utcnow().timestamp()

    return DeployHeader(
        accountPublicKey=params.accountPublicKey,
        body_hash=body.hash,
        chain_name=params.chain_name,
        dependencies=params.dependencies,
        gas_price=params.gas_price,
        timestamp=timestamp,
        ttl=params.ttl,
    )


def create_deploy_parameters(
    account: typing.Union[AccountInfo, PublicKey],
    chain_name: str,
    dependencies: typing.List[Digest] = [],
    gas_price: int = 1,
    timestamp: datetime.datetime = None,
    ttl: typing.Union[str, DeployTimeToLive] = "1day"
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
                 factory.accounts.create_public_key(account.algo, account.pbk)
    timestamp = timestamp or datetime.datetime.utcnow().timestamp()
    ttl = create_deploy_ttl(ttl) if isinstance(ttl, str) else ttl

    return DeployParameters(
        accountPublicKey=public_key,
        chain_name=chain_name,
        dependencies=dependencies,
        gas_price=gas_price,
        timestamp=timestamp,
        ttl=ttl,
    )


def create_deploy_ttl(humanized_ttl: str = "1day") -> DeployTimeToLive:
    """Returns a deploy's time to live after which it will not longer be accepted by a node.
    
    :param humanized_ttl: A humanized ttl, e.g. 1 day.

    """
    # TODO convert humanized to milliseconds.
    return DeployTimeToLive(humanized=humanized_ttl, as_milliseconds=1 * 24 * 60 * 60 * 1000)


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
        value = factory.create_cl_value(cl_type, parsed)
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
                factory.create_cl_type_of_simple(CLTypeKey.U512)
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
                factory.create_cl_type_of_simple(CLTypeKey.U512)
                ),
            create_execution_arg(
                "target",
                target,
                factory.create_cl_type_of_byte_array(32)
                ),
            create_execution_arg(
                "id",
                correlation_id,
                factory.create_cl_type_of_option(factory.create_cl_type_of_simple(CLTypeKey.U64))
                ),
        ]
    )
