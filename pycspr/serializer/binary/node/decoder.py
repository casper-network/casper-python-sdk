import typing

from pycspr.factory import create_public_key
from pycspr.serializer.binary.cl_type import decode as decode_cl_type
from pycspr.serializer.binary.cl_value import decode as decode_cl_value
from pycspr.types.cl import CLT_Type_ByteArray
from pycspr.types.cl import CLT_Type_U32
from pycspr.types.cl import CLT_Type_U64
from pycspr.types.cl import CLT_Type_List
from pycspr.types.cl import CLT_Type_PublicKey
from pycspr.types.cl import CLT_Type_String
from pycspr.types.crypto import KeyAlgorithm
from pycspr.types.node.rpc import Deploy
from pycspr.types.node.rpc import DeployApproval
from pycspr.types.node.rpc import DeployArgument
from pycspr.types.node.rpc import DeployBody
from pycspr.types.node.rpc import DeployExecutableItem
from pycspr.types.node.rpc import DeployHeader
from pycspr.types.node.rpc import DeployTimeToLive
from pycspr.types.node.rpc import DeployOfModuleBytes
from pycspr.types.node.rpc import DeployOfStoredContractByHash
from pycspr.types.node.rpc import DeployOfStoredContractByHashVersioned
from pycspr.types.node.rpc import DeployOfStoredContractByName
from pycspr.types.node.rpc import DeployOfStoredContractByNameVersioned
from pycspr.types.node.rpc import DeployOfTransfer
from pycspr.types.node.rpc import Timestamp
from pycspr.utils import convertor


def decode(bstream: bytes, typedef: object) -> typing.Tuple[bytes, object]:
    """Decoder: Domain entity <- an array of bytes.

    :param bstream: An array of bytes being decoded.
    :param typedef: Deploy related type definition.
    :returns: A deploy related type.

    """
    try:
        decoder = _DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from bytes")
    else:
        return decoder(bstream)


def _decode_deploy(bstream: bytes) -> typing.Tuple[bytes, Deploy]:
    bstream, header = decode(bstream, DeployHeader)
    bstream, deploy_hash = decode_cl_value(bstream, CLT_Type_ByteArray(32))
    bstream, payment = decode(bstream, DeployExecutableItem)
    bstream, session = decode(bstream, DeployExecutableItem)
    bstream, approvals = _decode_deploy_approval_set(bstream)

    return bstream, Deploy(
        approvals=approvals,
        hash=deploy_hash.value,
        header=header,
        payment=payment,
        session=session
    )


def _decode_deploy_approval(bstream: bytes) -> typing.Tuple[bytes, DeployApproval]:
    algo = KeyAlgorithm(bstream[0])
    if algo == KeyAlgorithm.ED25519:
        key_length = 32
    elif algo == KeyAlgorithm.SECP256K1:
        key_length = 33
    else:
        raise ValueError("Invalid Key Algorithm")
    pbk = bstream[1:key_length + 1]
    sig = bstream[key_length + 1:key_length + 66]
    bstream = bstream[1 + key_length + 66:]

    return bstream, DeployApproval(
        signer=create_public_key(algo, pbk),
        signature=sig
    )


def _decode_deploy_approval_set(
    bstream: bytes
) -> typing.Tuple[bytes, typing.List[DeployApproval]]:
    approvals = []
    bstream, args_length = decode_cl_value(bstream, CLT_Type_U32())
    for _ in range(args_length.value):
        bstream, approval = decode(bstream, DeployApproval)
        approvals.append(approval)

    return bstream, approvals


def _decode_deploy_argument(bstream: bytes) -> typing.Tuple[bytes, DeployArgument]:
    bstream, name = decode_cl_value(bstream, CLT_Type_String())
    bstream, val_bytes_length = decode_cl_value(bstream, CLT_Type_U32())
    bstream_rem, arg_cl_type = decode_cl_type(bstream[val_bytes_length.value:])
    _, arg_cl_value = decode_cl_value(bstream, arg_cl_type)

    return bstream_rem, DeployArgument(name.value, arg_cl_value)


def _decode_deploy_argument_set(
    bstream: bytes
) -> typing.Tuple[bytes, typing.List[DeployArgument]]:
    args = []
    bstream, args_length = decode_cl_value(bstream, CLT_Type_U32())
    for _ in range(args_length.value):
        bstream, arg = decode(bstream, DeployArgument)
        args.append(arg)

    return bstream, args


def _decode_deploy_body(bstream: bytes) -> typing.Tuple[bytes, DeployBody]:
    bstream, payment = _decode_deploy_executable_item(bstream)
    bstream, session = _decode_deploy_executable_item(bstream)
    bstream, body_hash = decode_cl_value(bstream, CLT_Type_ByteArray(32))

    return bstream, DeployBody(payment, session, body_hash.value)


def _decode_deploy_executable_item(bstream: bytes) -> DeployExecutableItem:
    if bstream[0] == 0:
        return decode(bstream, DeployOfModuleBytes)
    elif bstream[0] == 1:
        return decode(bstream, DeployOfStoredContractByHash)
    elif bstream[0] == 2:
        return decode(bstream, DeployOfStoredContractByHashVersioned)
    elif bstream[0] == 3:
        return decode(bstream, DeployOfStoredContractByName)
    elif bstream[0] == 4:
        return decode(bstream, DeployOfStoredContractByNameVersioned)
    elif bstream[0] == 5:
        return decode(bstream, DeployOfTransfer)

    raise ValueError("Invalid deploy executable item type tag")


def _decode_deploy_header(bstream: bytes) -> typing.Tuple[bytes, DeployHeader]:
    bstream, account_public_key = decode_cl_value(
        bstream, CLT_Type_PublicKey()
        )
    bstream, timestamp = decode(bstream, Timestamp)
    bstream, ttl = decode(bstream, DeployTimeToLive)
    bstream, gas_price = decode_cl_value(
        bstream, CLT_Type_U64()
        )
    bstream, body_hash = decode_cl_value(
        bstream, CLT_Type_ByteArray(32)
        )
    bstream, dependencies = decode_cl_value(
        bstream, CLT_Type_List(CLT_Type_ByteArray(32))
        )
    bstream, chain_name = decode_cl_value(
        bstream, CLT_Type_String()
        )

    return bstream, DeployHeader(
        account=account_public_key,
        body_hash=body_hash.value,
        chain_name=chain_name.value,
        dependencies=dependencies.vector,
        gas_price=gas_price.value,
        timestamp=timestamp,
        ttl=ttl
    )


def _decode_deploy_time_to_live(bstream: bytes) -> typing.Tuple[bytes, DeployTimeToLive]:
    bstream, ttl = decode_cl_value(
        bstream, CLT_Type_U64()
        )

    return bstream, DeployTimeToLive(
        ttl.value,
        convertor.humanized_time_interval_from_ms(ttl.value)
        )


def _decode_module_bytes(bstream: bytes) -> typing.Tuple[bytes, DeployOfModuleBytes]:
    bstream = bstream[1:]
    bstream, length = decode_cl_value(bstream, CLT_Type_U32())
    if length.value > 0:
        module_bytes = bstream[:length.value]
        bstream = bstream[length.value:]
    else:
        module_bytes = bytes([])
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, DeployOfModuleBytes(args, module_bytes)


def _decode_stored_contract_by_hash(
    bstream: bytes
) -> typing.Tuple[bytes, DeployOfStoredContractByHash]:
    bstream = bstream[1:]
    bstream, contract_hash = decode_cl_value(bstream, CLT_Type_ByteArray(32))
    bstream, entry_point = decode_cl_value(bstream, CLT_Type_String())
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, DeployOfStoredContractByHash(
        args=args,
        entry_point=entry_point.value,
        hash=contract_hash.value
        )


def _decode_stored_contract_by_hash_versioned(
    bstream: bytes
) -> typing.Tuple[bytes, DeployOfStoredContractByHashVersioned]:
    bstream = bstream[1:]
    bstream, contract_hash = decode_cl_value(bstream, CLT_Type_ByteArray(32))
    bstream, contract_version = decode_cl_value(bstream, CLT_Type_U32())
    bstream, entry_point = decode_cl_value(bstream, CLT_Type_String())
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, DeployOfStoredContractByHashVersioned(
        args=args,
        entry_point=entry_point.value,
        hash=contract_hash.value,
        version=contract_version.value
        )


def _decode_stored_contract_by_name(
    bstream: bytes
) -> typing.Tuple[bytes, DeployOfStoredContractByName]:
    bstream = bstream[1:]
    bstream, contract_name = decode_cl_value(bstream, CLT_Type_String())
    bstream, entry_point = decode_cl_value(bstream, CLT_Type_String())
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, DeployOfStoredContractByName(
        args=args,
        entry_point=entry_point.value,
        name=contract_name.value
        )


def _decode_stored_contract_by_name_versioned(
    bstream: bytes
) -> typing.Tuple[bytes, DeployOfStoredContractByNameVersioned]:
    bstream = bstream[1:]
    bstream, contract_name = decode_cl_value(bstream, CLT_Type_String())
    bstream, contract_version = decode_cl_value(bstream, CLT_Type_U32())
    bstream, entry_point = decode_cl_value(bstream, CLT_Type_String())
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, DeployOfStoredContractByNameVersioned(
        args=args,
        entry_point=entry_point.value,
        name=contract_name.value,
        version=contract_version.value
        )


def _decode_timestamp(bstream: bytes) -> typing.Tuple[bytes, Timestamp]:
    bstream, ts_ns = decode_cl_value(
        bstream, CLT_Type_U64()
        )

    return bstream, Timestamp(ts_ns.value / 1000)


def _decode_transfer(bstream: bytes) -> typing.Tuple[bytes, DeployOfTransfer]:
    bstream = bstream[1:]
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, DeployOfTransfer(args)


_DECODERS = {
    Deploy: _decode_deploy,
    DeployApproval: _decode_deploy_approval,
    DeployArgument: _decode_deploy_argument,
    DeployBody: _decode_deploy_body,
    DeployExecutableItem: _decode_deploy_executable_item,
    DeployHeader: _decode_deploy_header,
    DeployOfModuleBytes: _decode_module_bytes,
    DeployOfStoredContractByHash: _decode_stored_contract_by_hash,
    DeployOfStoredContractByHashVersioned: _decode_stored_contract_by_hash_versioned,
    DeployOfStoredContractByName: _decode_stored_contract_by_name,
    DeployOfStoredContractByNameVersioned: _decode_stored_contract_by_name_versioned,
    DeployOfTransfer: _decode_transfer,
    DeployTimeToLive: _decode_deploy_time_to_live,
    Timestamp: _decode_timestamp,
}
