import datetime
import random
import typing

from pycspr import crypto
from pycspr.factory.accounts import create_public_key
from pycspr.factory.digests import create_digest_of_deploy
from pycspr.factory.digests import create_digest_of_deploy_body
from pycspr.types import CL_Option
from pycspr.types import CL_PublicKey
from pycspr.types import CL_Type_U64
from pycspr.types import CL_U8
from pycspr.types import CL_U64
from pycspr.types import CL_U512
from pycspr.types import CL_URef
from pycspr.types import Deploy
from pycspr.types import DeployArgument
from pycspr.types import DeployApproval
from pycspr.types import DeployBody
from pycspr.types import DeployHeader
from pycspr.types import DeployParameters
from pycspr.types import DeployTimeToLive
from pycspr.types import DeployExecutableItem
from pycspr.types import ModuleBytes
from pycspr.types import PrivateKey
from pycspr.types import PublicKey
from pycspr.types import Timestamp
from pycspr.types import Transfer
from pycspr.types.cl_values import CL_Value
from pycspr.utils import constants
from pycspr.utils import conversion
from pycspr.utils import io as _io


def create_deploy(
    params: DeployParameters,
    payment: DeployExecutableItem,
    session: DeployExecutableItem
):
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
        approver.as_public_key,
        crypto.get_signature_for_deploy_approval(
            deploy_hash, approver.private_key, approver.key_algo
            )
    )


def create_deploy_arguments(args: typing.Dict[str, CL_Value]) -> typing.List[DeployArgument]:
    """Returns a collection of deploy arguments for interpretation by a node.

    :param args: Dictionary of argument name & cl-value pairs.
    :returns: A collection of deploy arguments for interpretation by a node.

    """
    return [DeployArgument(k, v) for (k, v) in args.items()]


def create_deploy_body(
    payment: DeployExecutableItem,
    session: DeployExecutableItem
) -> DeployBody:
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
    public_key = \
        account if isinstance(account, PublicKey) else \
        create_public_key(account.algo, account.pbk)
    timestamp = timestamp or datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    timestamp = Timestamp(round(timestamp, 3))
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
    as_milliseconds = conversion.humanized_time_interval_to_milliseconds(humanized_ttl)
    if as_milliseconds > constants.DEPLOY_TTL_MS_MAX:
        raise ValueError(f"Invalid deploy ttl. Maximum (ms) = {constants.DEPLOY_TTL_MS_MAX}")

    return DeployTimeToLive(
        humanized=humanized_ttl,
        as_milliseconds=as_milliseconds
    )


def create_standard_payment(
    amount: int = constants.STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS
) -> ModuleBytes:
    """Returns standard payment execution information.

    :param amount: Maximum amount in motes to be used for standard payment.

    """
    return ModuleBytes(
        args={
            "amount": CL_U512(amount)
        },
        module_bytes=bytes([])
        )


def create_transfer(
    params: DeployParameters,
    amount: int,
    target: bytes,
    correlation_id: int = None,
    payment: int = constants.STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS
) -> Deploy:
    """Returns a native transfer deploy.

    :param params: Standard parameters used when creating a deploy.
    :param amount: Amount in motes to be transferred.
    :param target: Target account key.
    :param correlation_id: Identifier used to correlate transfer to internal systems.
    :returns: A native transfer deploy.

    """
    return create_deploy(
        params,
        create_standard_payment(payment),
        create_transfer_session(amount, target, correlation_id)
        )


def create_transfer_session(
    amount: int,
    target: bytes,
    correlation_id: int = None,
) -> Transfer:
    """Returns session execution information for a native transfer.

    :param amount: Amount in motes to be transferred.
    :param target: Target account key.
    :param correlation_id: Identifier used to correlate transfer to internal systems.
    :returns: A native transfer session logic.

    """
    correlation_id = correlation_id or random.randint(1, constants.MAX_TRANSFER_ID)
    return Transfer(
        args={
            "amount": CL_U512(amount),
            "target": CL_PublicKey.from_account_key(target),
            "id": CL_Option(CL_U64(correlation_id), CL_Type_U64()),
        }
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
    session = ModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args={
            "amount": CL_U512(amount),
            "delegation_rate": CL_U8(delegation_rate),
            "public_key": CL_PublicKey.from_public_key(public_key),
        }
    )

    return create_deploy(params, payment, session)


def create_validator_auction_bid_withdrawal(
    params: DeployParameters,
    amount: int,
    public_key: PublicKey,
    path_to_wasm: str,
    unbond_purse_ref: typing.Union[CL_URef, str],
) -> Deploy:
    """Returns an auction bid withdraw delegation deploy.

    :param params: Standard parameters used when creating a deploy.
    :param amount: Amount in motes to be withdrawn from auction.
    :param public_key: Public key of validator.
    :param path_to_wasm: Path to compiled delegate.wasm.
    :param unbond_purse_ref: Validator's purse unforgeable reference to which to withdraw funds.
    :returns: A standard delegation deploy.

    """
    payment = create_standard_payment(constants.STANDARD_PAYMENT_FOR_AUCTION_BID_WITHDRAWAL)
    session = ModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args={
            "amount": CL_U512(amount),
            "public_key": CL_PublicKey.from_public_key(public_key),
            "unbond_purse":
                unbond_purse_ref if isinstance(unbond_purse_ref, CL_URef) else
                CL_URef.from_string(unbond_purse_ref)
        }
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
    session = ModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args=[
            DeployArgument(
                "amount",
                CL_U512(amount)
                ),
            DeployArgument(
                "delegator",
                CL_PublicKey.from_public_key(public_key_of_delegator)
                ),
            DeployArgument(
                "validator",
                CL_PublicKey.from_public_key(public_key_of_validator)
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
    session = ModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args={
            "amount": CL_U512(amount),
            "delegator": CL_PublicKey.from_public_key(public_key_of_delegator),
            "validator": CL_PublicKey.from_public_key(public_key_of_validator)
        }
    )

    return create_deploy(params, payment, session)
