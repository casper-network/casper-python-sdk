import typing

from pycspr.crypto import KeyAlgorithm
from pycspr.factory import create_public_key
from pycspr.serialisation.cl_type_from_bytes import decode as cl_type_from_bytes
from pycspr.serialisation.cl_value_from_bytes import decode as cl_value_from_bytes
from pycspr.types import Timestamp
from pycspr.types import cl_types
from pycspr.types import Deploy
from pycspr.types import DeployApproval
from pycspr.types import DeployArgument
from pycspr.types import DeployBody
from pycspr.types import DeployExecutableItem
from pycspr.types import DeployHeader
from pycspr.types import DeployTimeToLive
from pycspr.types import ModuleBytes
from pycspr.types import StoredContractByHash
from pycspr.types import StoredContractByHashVersioned
from pycspr.types import StoredContractByName
from pycspr.types import StoredContractByNameVersioned
from pycspr.types import Transfer


def decode(bstream: bytes, typedef: object) -> typing.Tuple[bytes, object]:
    """Decodes a deploy from a byte array.

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
    bstream, deploy_hash = cl_value_from_bytes(bstream, cl_types.CL_Type_ByteArray(32))
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


def _decode_deploy_approval_set(bstream: bytes) -> typing.Tuple[bytes, typing.List[DeployApproval]]:
    approvals = []
    bstream, args_length = cl_value_from_bytes(bstream, cl_types.CL_Type_U32())
    for _ in range(args_length.value):        
        bstream, approval = decode(bstream, DeployApproval)
        approvals.append(approval)

    return bstream, approvals


def _decode_deploy_argument(bstream: bytes) -> typing.Tuple[bytes, DeployArgument]:
    bstream, name = cl_value_from_bytes(bstream, cl_types.CL_Type_String())
    bstream, val_bytes_length = cl_value_from_bytes(bstream, cl_types.CL_Type_U32())
    bstream_rem, arg_cl_type = cl_type_from_bytes(bstream[val_bytes_length.value:])
    _, arg_cl_value = cl_value_from_bytes(bstream, arg_cl_type)

    return bstream_rem, DeployArgument(name.value, arg_cl_value)


def _decode_deploy_argument_set(bstream: bytes) -> typing.Tuple[bytes, typing.List[DeployArgument]]:
    args = []
    bstream, args_length = cl_value_from_bytes(bstream, cl_types.CL_Type_U32())
    for _ in range(args_length.value):        
        bstream, arg = decode(bstream, DeployArgument)
        args.append(arg)

    return bstream, args


def _decode_deploy_body(bstream: bytes) -> typing.Tuple[bytes, DeployBody]:
    bstream, payment = _decode_deploy_executable_item(bstream)
    bstream, session = _decode_deploy_executable_item(bstream)
    bstream, body_hash = cl_value_from_bytes(bstream, cl_types.CL_Type_ByteArray(32))

    return bstream, DeployBody(payment, session, body_hash.value)


def _decode_deploy_executable_item(bstream: bytes) -> DeployExecutableItem:
    if bstream[0] == 0:
        return decode(bstream, ModuleBytes)
    elif bstream[0] == 1:
        return decode(bstream, StoredContractByHash)
    elif bstream[0] == 2:
        return decode(bstream, StoredContractByHashVersioned)
    elif bstream[0] == 3:
        return decode(bstream, StoredContractByName)
    elif bstream[0] == 4:
        return decode(bstream, StoredContractByNameVersioned)
    elif bstream[0] == 5:
        return decode(bstream, Transfer)

    raise ValueError("Invalid deploy executable item type tag")


def _decode_deploy_header(bstream: bytes) -> typing.Tuple[bytes, DeployHeader]:
    bstream, account_public_key = cl_value_from_bytes(
        bstream, cl_types.CL_Type_PublicKey()
        )
    bstream, timestamp = cl_value_from_bytes(
        bstream, cl_types.CL_Type_U64()
        )
    bstream, ttl = cl_value_from_bytes(
        bstream, cl_types.CL_Type_U64()
        )
    bstream, gas_price = cl_value_from_bytes(
        bstream, cl_types.CL_Type_U64()
        )
    bstream, body_hash = cl_value_from_bytes(
        bstream, cl_types.CL_Type_ByteArray(32)
        )
    bstream, dependencies = cl_value_from_bytes(
        bstream, cl_types.CL_Type_List(cl_types.CL_Type_ByteArray(32))
        )
    bstream, chain_name = cl_value_from_bytes(
        bstream, cl_types.CL_Type_String()
        )

    return bstream, DeployHeader(
        account_public_key=account_public_key,
        body_hash=body_hash.value,
        chain_name=chain_name.value,
        dependencies=dependencies.vector,
        gas_price=gas_price.value,
        timestamp=Timestamp(timestamp.value / 1000),
        ttl=DeployTimeToLive.from_milliseconds(ttl.value)
    )


def _decode_module_bytes(bstream: bytes) -> typing.Tuple[bytes, ModuleBytes]:
    bstream = bstream[1:]
    bstream, length = cl_value_from_bytes(bstream, cl_types.CL_Type_U32())
    if length.value > 0:
        module_bytes = bstream[:length.value]
        bstream = bstream[length.value:]
    else:
        module_bytes = bytes([])
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, ModuleBytes(args, module_bytes)


def _decode_stored_contract_by_hash(bstream: bytes) -> typing.Tuple[bytes, StoredContractByHash]:
    bstream = bstream[1:]
    bstream, contract_hash = cl_value_from_bytes(bstream, cl_types.CL_Type_ByteArray(32))
    bstream, entry_point = cl_value_from_bytes(bstream, cl_types.CL_Type_String())
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, StoredContractByHash(
        args=args, 
        entry_point=entry_point.value, 
        hash=contract_hash.value
        )


def _decode_stored_contract_by_hash_versioned(bstream: bytes) -> typing.Tuple[bytes, StoredContractByHashVersioned]:
    bstream = bstream[1:]
    bstream, contract_hash = cl_value_from_bytes(bstream, cl_types.CL_Type_ByteArray(32))
    bstream, contract_version = cl_value_from_bytes(bstream, cl_types.CL_Type_U32())
    bstream, entry_point = cl_value_from_bytes(bstream, cl_types.CL_Type_String())
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, StoredContractByHashVersioned(
        args=args, 
        entry_point=entry_point.value, 
        hash=contract_hash.value,
        version=contract_version.value
        )


def _decode_stored_contract_by_name(bstream: bytes) -> typing.Tuple[bytes, StoredContractByName]:
    bstream = bstream[1:]
    bstream, contract_name = cl_value_from_bytes(bstream, cl_types.CL_Type_String())
    bstream, entry_point = cl_value_from_bytes(bstream, cl_types.CL_Type_String())
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, StoredContractByName(
        args=args, 
        entry_point=entry_point.value, 
        name=contract_name.value
        )


def _decode_stored_contract_by_name_versioned(bstream: bytes) -> typing.Tuple[bytes, StoredContractByNameVersioned]:
    bstream = bstream[1:]
    bstream, contract_name = cl_value_from_bytes(bstream, cl_types.CL_Type_String())
    bstream, contract_version = cl_value_from_bytes(bstream, cl_types.CL_Type_U32())
    bstream, entry_point = cl_value_from_bytes(bstream, cl_types.CL_Type_String())
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, StoredContractByNameVersioned(
        args=args, 
        entry_point=entry_point.value, 
        name=contract_name.value,
        version=contract_version.value
        )


def _decode_transfer(bstream: bytes) -> typing.Tuple[bytes, Transfer]:
    bstream = bstream[1:]
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, Transfer(args)


_DECODERS = {
    Deploy: _decode_deploy,
    DeployApproval: _decode_deploy_approval,
    DeployArgument: _decode_deploy_argument,
    DeployBody: _decode_deploy_body,
    DeployExecutableItem: _decode_deploy_executable_item,
    DeployHeader: _decode_deploy_header,
    ModuleBytes: _decode_module_bytes,
    StoredContractByHash: _decode_stored_contract_by_hash,
    StoredContractByHashVersioned: _decode_stored_contract_by_hash_versioned,
    StoredContractByName: _decode_stored_contract_by_name,
    StoredContractByNameVersioned: _decode_stored_contract_by_name_versioned,
    Transfer: _decode_transfer
}