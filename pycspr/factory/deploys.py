import datetime
import random
import typing

from pycspr.type_defs.crypto import PrivateKey, PublicKey
from pycspr.crypto import get_signature_for_deploy_approval
from pycspr.factory.digests import create_digest_of_deploy, create_digest_of_deploy_body
from pycspr.types.node import \
    Deploy, \
    DeployBody, \
    DeployHeader, \
    DeployParameters, \
    DeployTimeToLive
from pycspr.type_defs.cl_types import CLT_U64
from pycspr.type_defs.cl_values import \
    CLV_U8, \
    CLV_U64, \
    CLV_U512, \
    CLV_PublicKey, \
    CLV_URef, \
    CLV_Value
from pycspr.types.node import \
    DeployApproval, \
    DeployArgument, \
    DeployExecutableItem, \
    DeployOfModuleBytes, \
    DeployOfTransfer, \
    Timestamp
from pycspr.utils import constants, convertor, io as _io


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
        approver.to_public_key(),
        get_signature_for_deploy_approval(deploy_hash, approver)
    )


def create_deploy_arguments(args: typing.Dict[str, CLV_Value]) -> typing.List[DeployArgument]:
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
        account=params.account,
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
    gas_price: int = constants.DEFAULT_TX_GAS_PRICE,
    timestamp: datetime.datetime = None,
    ttl: typing.Union[str, DeployTimeToLive] = constants.DEFAULT_TX_TTL
) -> DeployParameters:
    """Returns header information associated with a deploy.

    :param account: Account dispatching deploy.
    :param chain_name: Identifier of target chain.
    :param dependencies: Array of hashes of deploys that must be processed prior to this one.
    :param gas_price: Array of hashes of deploys that must be processed prior to this one.
    :param timestamp: Milliseconds since epoch when deploy was instantiated.
    :param ttl: Humanized time interval prior to which deploy must be processed.

    """
    public_key = account if isinstance(account, PublicKey) else account.to_public_key()
    timestamp = timestamp or datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    timestamp = Timestamp(round(timestamp, 3))
    ttl = create_deploy_ttl(ttl) if isinstance(ttl, str) else ttl

    return DeployParameters(
        account=public_key,
        chain_name=chain_name,
        dependencies=dependencies,
        gas_price=gas_price,
        timestamp=timestamp,
        ttl=ttl,
    )


def create_deploy_ttl(humanized_ttl: str = constants.DEFAULT_TX_TTL) -> DeployTimeToLive:
    """Returns a deploy's time to live after which it will not longer be accepted by a node.

    :param humanized_ttl: A humanized ttl, e.g. 2 hours.

    """
    as_milliseconds = convertor.ms_from_humanized_time_interval(humanized_ttl)
    if as_milliseconds > constants.TX_MAX_TTL_MS:
        raise ValueError(
            f"Invalid deploy ttl. Max={constants.TX_MAX_TTL_MS}ms. Actual={humanized_ttl}."
            )

    return DeployTimeToLive(
        humanized=humanized_ttl,
        as_milliseconds=as_milliseconds
    )


def create_standard_payment(
    amount: int = constants.STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS
) -> DeployOfModuleBytes:
    """Returns standard payment execution information.

    :param amount: Maximum amount in motes to be used for standard payment.

    """
    return DeployOfModuleBytes(
        args={
            "amount":
                CLV_U512(amount)
        },
        module_bytes=bytes([])
        )


def create_transfer(
    params: DeployParameters,
    amount: int,
    target: PublicKey,
    correlation_id: int = None,
    payment: int = constants.STANDARD_PAYMENT_FOR_NATIVE_TRANSFERS
) -> Deploy:
    """Returns a native transfer deploy.

    :param params: Standard parameters used when creating a deploy.
    :param amount: Amount in motes to be transferred.
    :param target: Public key of target account.
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
    target: PublicKey,
    correlation_id: int = None,
) -> DeployOfTransfer:
    """Returns session execution information for a native transfer.

    :param amount: Amount in motes to be transferred.
    :param target: Public key of target account.
    :param correlation_id: Identifier used to correlate transfer to internal systems.
    :returns: A native transfer session logic.

    """
    correlation_id = correlation_id or random.randint(1, constants.MAX_TRANSFER_ID)

    return DeployOfTransfer(
        args={
            "amount":
                CLV_U512(amount),
            "target":
                CLV_PublicKey.from_public_key(target),
            "id":
                CLV_Option(CLV_U64(correlation_id), CLT_U64()),
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
    session = DeployOfModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args={
            "amount":
                CLV_U512(amount),
            "delegation_rate":
                CLV_U8(delegation_rate),
            "public_key":
                CLV_PublicKey.from_public_key(public_key),
        }
    )

    return create_deploy(params, payment, session)


def create_validator_auction_bid_withdrawal(
    params: DeployParameters,
    amount: int,
    public_key: PublicKey,
    path_to_wasm: str,
    unbond_purse_ref: typing.Union[CLV_URef, str],
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
    session = DeployOfModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args={
            "amount":
                CLV_U512(amount),
            "public_key":
                CLV_PublicKey.from_public_key(public_key),
            "unbond_purse":
                CLV_URef.from_str(unbond_purse_ref) if isinstance(unbond_purse_ref, str) else
                unbond_purse_ref
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
    session = DeployOfModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args={
            "amount":
                CLV_U512(amount),
            "delegator":
                CLV_PublicKey.from_public_key(public_key_of_delegator),
            "validator":
                CLV_PublicKey.from_public_key(public_key_of_validator),
        }
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
    session = DeployOfModuleBytes(
        module_bytes=_io.read_wasm(path_to_wasm),
        args={
            "amount":
                CLV_U512(amount),
            "delegator":
                CLV_PublicKey.from_public_key(public_key_of_delegator),
            "validator":
                CLV_PublicKey.from_public_key(public_key_of_validator)
        }
    )

    return create_deploy(params, payment, session)
