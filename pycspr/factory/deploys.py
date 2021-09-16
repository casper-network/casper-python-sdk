import datetime
import pathlib
import typing

from pycspr import crypto
from pycspr.factory.accounts import create_public_key
from pycspr.factory.cl import create_cl_type_of_byte_array
from pycspr.factory.cl import create_cl_type_of_option
from pycspr.factory.cl import create_cl_type_of_simple
from pycspr.factory.cl import create_cl_value
from pycspr.factory.digests import create_digest_of_deploy
from pycspr.factory.digests import create_digest_of_deploy_body
from pycspr.types import PrivateKey
from pycspr.types import CLAccessRights
from pycspr.types import CLTypeKey
from pycspr.types import CLType
from pycspr.types import Deploy
from pycspr.types import DeployApproval
from pycspr.types import DeployBody
from pycspr.types import DeployHeader
from pycspr.types import DeployParameters
from pycspr.types import DeployTimeToLive
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutableDeployItem
from pycspr.types import ExecutableDeployItem_ModuleBytes
from pycspr.types import ExecutableDeployItem_Transfer
from pycspr.types import PublicKey
from pycspr.types import UnforgeableReference
from pycspr.utils import constants
from pycspr.utils import conversion
from pycspr.utils import io as _io



def create_deploy(params: DeployParameters, payment: ExecutableDeployItem, session: ExecutableDeployItem):
    """Returns a deploy for subsequent dispatch to a node.
    
    :param params: Standard parameters used when creating a deploy.
    :param session: Session execution information.
    :param payment: Payment execution information.

    """
    body = create_deploy_body(payment, session)
    header = create_deploy_header(body, params)

    return Deploy(
        approvals=[],
        hash=create_digest_of_deploy(header),
        header=header,
        payment=payment,
        session=session
    )


def create_deploy_approval(deploy: typing.Union[bytes, Deploy], approver: PrivateKey):
    """Returns a deploy approval to be associated with a deploy.
    
    :param deploy: Either a deploy to be approved, or the hash of a deploy to be approved.
    :param approver: Account key of entity approving a deploy.
    :returns: A deploy approval to be associated with a deploy.

    """
    deploy_hash = deploy.hash if isinstance(deploy, Deploy) else deploy
    assert len(deploy_hash) == 32, "Invalid deploy hash"

    return DeployApproval(
        approver.account_key,
        crypto.get_signature_for_deploy_approval(deploy_hash, approver.private_key, approver.key_algo)
    )


def create_deploy_argument(
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


def create_deploy_body(payment: ExecutableDeployItem, session: ExecutableDeployItem) -> DeployBody:
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
        account_public_key=params.account_public_key,
        body_hash=body.hash,
        chain_name=params.chain_name,
        dependencies=params.dependencies,
        gas_price=params.gas_price,
        timestamp=params.timestamp,
        ttl=params.ttl,
    )


def create_deploy_parameters(
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
    public_key = account if isinstance(account, PublicKey) else \
                 create_public_key(account.algo, account.pbk)
    if timestamp is None:
        timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    timestamp = round(timestamp, 3)
    ttl = create_deploy_ttl(ttl) if isinstance(ttl, str) else ttl

    return DeployParameters(
        account_public_key=public_key,
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
    humanized_ttl="1day"
    as_milliseconds = conversion.humanized_time_interval_to_milliseconds(humanized_ttl)
    if as_milliseconds > constants.DEPLOY_TTL_MS_MAX:
        raise ValueError(f"Invalid deploy ttl {humanized_ttl} = {as_milliseconds} ms.  Maximum (ms) = {constants.DEPLOY_TTL_MS_MAX}")

    return DeployTimeToLive(
        humanized=humanized_ttl,
        as_milliseconds=as_milliseconds
    )


def create_native_transfer(
    params: DeployParameters,
    amount: int,
    target: bytes,
    correlation_id: int,
    ) -> Deploy:
    """Returns a native transfer deploy.

    :param params: Standard parameters used when creating a deploy.
    :param amount: Amount in motes to be transferred.
    :param target: Target account hash.
    :param correlation_id: An identifier used by dispatcher to subsequently correlate the transfer to internal systems.
    :returns: A native transfer deploy.

    """
    return create_deploy(
        params,
        create_standard_payment(constants.STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS),
        create_native_transfer_session(amount, target, correlation_id)
        )


def create_native_transfer_session(
    amount: int,
    target: bytes,
    correlation_id: int,
    ) -> ExecutableDeployItem_Transfer:
    """Returns session execution information for a native transfer.

    :param amount: Amount in motes to be transferred.
    :param target: Target account hash.
    :param correlation_id: An identifier used by dispatcher to subsequently correlate the transfer to internal systems.
    
    """
    return ExecutableDeployItem_Transfer(
        args=[
            create_deploy_argument(
                "amount",
                amount,
                create_cl_type_of_simple(CLTypeKey.U512)
                ),
            create_deploy_argument(
                "target",
                target,
                create_cl_type_of_byte_array(32)
                ),
            create_deploy_argument(
                "id",
                correlation_id,
                create_cl_type_of_option(create_cl_type_of_simple(CLTypeKey.U64))
                ),
        ]
    )


def create_standard_payment(
    amount: int = constants.STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS
    ) -> ExecutableDeployItem_ModuleBytes:
    """Returns standard payment execution information.
    
    :param amount: Maximum amount in motes to be used for standard payment.

    """
    return ExecutableDeployItem_ModuleBytes(
        args=[
            create_deploy_argument(
                "amount",
                amount,
                create_cl_type_of_simple(CLTypeKey.U512)
                ),
        ],
        module_bytes=bytes([])
        )


def create_uref_from_string(as_string: str):
    """Returns an unforgeable reference from it's string representation.
    
    """
    _, address_hex, access_rights = as_string.split("-")

    return UnforgeableReference(
        bytes.fromhex(address_hex),
        CLAccessRights(int(access_rights))
        )


def create_validator_auction_bid(
    params: DeployParameters,
    amount: int,
    delegation_rate: int,
    public_key: PublicKey,
    path_to_wasm: str
    ) -> Deploy:
    """Returns a validator auction bid deploy.

    :param params: Standard parameters used when creating a deploy.
    :param amount: Amount in motes to be submitted as an auction bid.
    :param delegation_rate: Percentage charged to a delegator for provided service.
    :param public_key: Public key of validator.
    :param path_to_wasm: Path to compiled delegate.wasm.
    :returns: A standard delegation deploy.

    """
    payment = create_standard_payment(constants.STANDARD_PAYMENT_FOR_AUCTION_BID)
    session = ExecutableDeployItem_ModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args=[
            create_deploy_argument(
                "amount",
                amount,
                create_cl_type_of_simple(CLTypeKey.U512)
                ),
            create_deploy_argument(
                "delegation_rate",
                delegation_rate,
                create_cl_type_of_simple(CLTypeKey.U8)
                ),
            create_deploy_argument(
                "public_key",
                public_key,
                create_cl_type_of_simple(CLTypeKey.PUBLIC_KEY)
                ),
            ]
        )
    
    return create_deploy(params, payment, session)


def create_validator_auction_bid_withdrawal(
    params: DeployParameters,
    amount: int,
    public_key: PublicKey,    
    path_to_wasm: str,
    unbond_purse: str,
    ) -> Deploy:
    """Returns an auction bid withdraw delegation deploy.

    :param params: Standard parameters used when creating a deploy.
    :param amount: Amount in motes to be withdrawn from auction.
    :param public_key: Public key of validator.
    :param path_to_wasm: Path to compiled delegate.wasm.
    :param unbond_purse: Validator's purse to which to withdraw funds.
    :returns: A standard delegation deploy.

    """
    payment = create_standard_payment(constants.STANDARD_PAYMENT_FOR_AUCTION_BID_WITHDRAWAL)
    session = ExecutableDeployItem_ModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args=[
            create_deploy_argument(
                "public_key",
                public_key,
                create_cl_type_of_simple(CLTypeKey.PUBLIC_KEY)
                ),
            create_deploy_argument(
                "amount",
                amount,
                create_cl_type_of_simple(CLTypeKey.U512)
                ),
            create_deploy_argument(
                "unbond_purse",
                unbond_purse,
                create_cl_type_of_option(create_cl_type_of_simple(CLTypeKey.UREF))
                ),
            ]
        )

    return create_deploy(params, payment, session)


def create_validator_delegation(
    params: DeployParameters,
    amount: int,
    public_key_of_delegator: PublicKey,
    public_key_of_validator: PublicKey,
    path_to_wasm: str
    ) -> Deploy:
    """Returns a standard delegation deploy.

    :param params: Standard parameters used when creating a deploy.
    :param amount: Amount in motes to be delegated.
    :param public_key_of_delegator: Public key of delegator.
    :param public_key_of_validator: Public key of validator.
    :param path_to_wasm: Path to compiled delegate.wasm.
    :returns: A standard delegation deploy.

    """
    payment = create_standard_payment(constants.STANDARD_PAYMENT_FOR_DELEGATION)
    session = ExecutableDeployItem_ModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args=[
            create_deploy_argument(
                "amount",
                amount,
                create_cl_type_of_simple(CLTypeKey.U512)
                ),
            create_deploy_argument(
                "delegator",
                public_key_of_delegator,
                create_cl_type_of_simple(CLTypeKey.PUBLIC_KEY)
                ),
            create_deploy_argument(
                "validator",
                public_key_of_validator,
                create_cl_type_of_simple(CLTypeKey.PUBLIC_KEY)
                ),
        ]
    )

    return create_deploy(params, payment, session)


def create_validator_delegation_withdrawal(
    params: DeployParameters,
    amount: int,
    public_key_of_delegator: PublicKey,
    public_key_of_validator: PublicKey,
    path_to_wasm: str
    ) -> Deploy:
    """Returns a standard withdraw delegation deploy.

    :param params: Standard parameters used when creating a deploy.
    :param amount: Amount in motes to be delegated.
    :param public_key_of_delegator: Public key of delegator.
    :param public_key_of_validator: Public key of validator.
    :param path_to_wasm: Path to compiled delegate.wasm.
    :returns: A standard delegation deploy.

    """
    payment = create_standard_payment(constants.STANDARD_PAYMENT_FOR_DELEGATION_WITHDRAWAL)
    session = ExecutableDeployItem_ModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args=[
            create_deploy_argument(
                "amount",
                amount,
                create_cl_type_of_simple(CLTypeKey.U512)
                ),
            create_deploy_argument(
                "delegator",
                public_key_of_delegator,
                create_cl_type_of_simple(CLTypeKey.PUBLIC_KEY)
                ),
            create_deploy_argument(
                "validator",
                public_key_of_validator,
                create_cl_type_of_simple(CLTypeKey.PUBLIC_KEY)
                ),
        ]
    )

    return create_deploy(params, payment, session)
