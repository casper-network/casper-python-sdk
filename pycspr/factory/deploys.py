import datetime
import typing

from pycspr import crypto
from pycspr.types.account import AccountKeyInfo
from pycspr.types.cl import CLType
from pycspr.types.cl import CLTypeInfo
from pycspr.types.cl import CLValue
from pycspr.types.deploy import Deploy
from pycspr.types.deploy import Digest
from pycspr.types.deploy import DeployApproval
from pycspr.types.deploy import DeployHeader
from pycspr.types.deploy import DeployExecutable_ModuleBytes
from pycspr.types.deploy import DeployExecutable_Transfer
from pycspr.types.deploy import DeployNamedArg

from pycspr.factory import cl_type_info


def create_approval(
    account_key_info: AccountKeyInfo, 
    data: bytes
    ) -> DeployApproval:
    """Returns an approval authorizing a node to process a deploy.
    
    """
    return DeployApproval(
        signer=account_key_info.public_key, 
        signature=crypto.get_signature(
            data,
            account_key_info.private_key,
            algo=account_key_info.algo
            )
        )


def create_cl_value(cl_type: CLType, value: object) -> CLValue:
    """Returns an arbitrary value encoded for interpretation by a node.
    
    """
    # TODO: map value to bytes
    return CLValue(
        bytes = bytes([]),
        cl_type = cl_type
    )


def create_deploy(approvals, header, payment, session):
    return Deploy(
        approvals=approvals,
        hash=None,
        header=header,
        payment=payment,
        session=session
    )


def create_header(
    account_key_info: AccountKeyInfo,
    body_hash: Digest,
    chain_name: str,
    dependencies: typing.List[Digest] = [],
    timestamp: datetime.datetime = None,
    ttl: str = "1day"
    ) -> DeployHeader:
    """Returns header information associated with a deploy.
    
    """
    return DeployHeader(
        account=account_key_info.account_key,
        timestamp=timestamp or datetime.datetime.utcnow(),
        ttl=ttl,
        body_hash=body_hash,
        dependencies=dependencies,
        chain_name=chain_name,
    )


def create_named_arg(
    name: str,
    value: object, 
    cl_type: typing.Union[CLType, CLTypeInfo]
    ) -> DeployNamedArg:
    """Returns a named argument associated with deploy execution information (session|payment).
    
    """
    type_info = CLTypeInfo(cl_type) if isinstance(cl_type, CLType) else cl_type
    print(type_info)

    return DeployNamedArg(
        cl_type_info = CLTypeInfo(cl_type) if isinstance(cl_type, CLType) else cl_type,
        name = name,
        value = value,
    )


def create_payment_for_transfer(amount: int = 10000) -> DeployExecutable_ModuleBytes:
    """Returns payment execution info for a native transfer.
    
    """
    return DeployExecutable_ModuleBytes(
        args=[
            create_named_arg("amount", amount, CLType.U512),
        ],
        module_bytes=bytes([])
        )


def create_session_for_transfer(
    amount: int,
    target: bytes,
    correlation_id: int,
    ) -> DeployExecutable_Transfer:
    """Returns session execution info for a native transfer.
    
    """
    return DeployExecutable_Transfer(
        args=[
            create_named_arg(
                "amount",
                amount,
                CLType.U512
                ),
            create_named_arg(
                "target",
                target,
                CLType.PUBLIC_KEY
                ),
            create_named_arg(
                "id",
                correlation_id,
                CLType.U64
                ),
        ]
    )
