import typing

from pycspr.serializer.binary.decoder_clt import decode as decode_clt
from pycspr.serializer.binary.decoder_clv import decode as decode_clv
from pycspr.type_defs.cl_types import CLT_ByteArray
from pycspr.type_defs.cl_types import CLT_U32
from pycspr.type_defs.cl_types import CLT_U64
from pycspr.type_defs.cl_types import CLT_List
from pycspr.type_defs.cl_types import CLT_PublicKey
from pycspr.type_defs.cl_types import CLT_String
from pycspr.type_defs.crypto import KeyAlgorithm
from pycspr.type_defs.crypto import PublicKey
from pycspr.type_defs.crypto import Signature
from pycspr.types.node import Deploy
from pycspr.types.node import DeployApproval
from pycspr.types.node import DeployArgument
from pycspr.types.node import DeployBody
from pycspr.types.node import DeployExecutableItem
from pycspr.types.node import DeployHeader
from pycspr.types.node import DeployTimeToLive
from pycspr.types.node import DeployOfModuleBytes
from pycspr.types.node import DeployOfStoredContractByHash
from pycspr.types.node import DeployOfStoredContractByHashVersioned
from pycspr.types.node import DeployOfStoredContractByName
from pycspr.types.node import DeployOfStoredContractByNameVersioned
from pycspr.types.node import DeployOfTransfer
from pycspr.types.node import Timestamp
from pycspr.utils import convertor


def decode(typedef: object, bstream: bytes) -> typing.Tuple[bytes, object]:
    """Decoder: Domain entity <- an array of bytes.

    :param typedef: Domain entity type definition.
    :param bstream: An array of bytes being decoded.
    :returns: A Domain entity type instance.

    """
    try:
        decoder = _DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from bytes")
    else:
        return decoder(bstream)


def _decode_deploy(bstream: bytes) -> typing.Tuple[bytes, Deploy]:
    bstream, header = decode(DeployHeader, bstream)
    bstream, deploy_hash = decode_clv(CLT_ByteArray(32), bstream)
    bstream, payment = decode(DeployExecutableItem, bstream)
    bstream, session = decode(DeployExecutableItem, bstream)
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
        pbk_length: int = 32
    elif algo == KeyAlgorithm.SECP256K1:
        pbk_length: int = 33
    else:
        raise ValueError("Invalid Key Algorithm")

    return \
        bstream[1 + pbk_length + 66:], \
        DeployApproval(
            signer=PublicKey.from_bytes(bstream[:pbk_length + 1]),
            signature=Signature.from_bytes(bstream[pbk_length + 1:pbk_length + 66])
        )


def _decode_deploy_approval_set(
    bstream: bytes
) -> typing.Tuple[bytes, typing.List[DeployApproval]]:
    approvals = []
    bstream, args_length = decode_clv(CLT_U32(), bstream)
    for _ in range(args_length.value):
        bstream, approval = decode(DeployApproval, bstream)
        approvals.append(approval)

    return bstream, approvals


def _decode_deploy_argument(bstream: bytes) -> typing.Tuple[bytes, DeployArgument]:
    bstream, name = decode_clv(CLT_String(), bstream)
    bstream, val_bytes_length = decode_clv(CLT_U32(), bstream)
    bstream_rem, arg_typedef = decode_clt(bstream[val_bytes_length.value:])
    _, arg_clv = decode_clv(arg_typedef, bstream)

    return bstream_rem, DeployArgument(name.value, arg_clv)


def _decode_deploy_argument_set(
    bstream: bytes
) -> typing.Tuple[bytes, typing.List[DeployArgument]]:
    args = []
    bstream, args_length = decode_clv(CLT_U32(), bstream)
    for _ in range(args_length.value):
        bstream, arg = decode(DeployArgument, bstream)
        args.append(arg)

    return bstream, args


def _decode_deploy_body(bstream: bytes) -> typing.Tuple[bytes, DeployBody]:
    bstream, payment = _decode_deploy_executable_item(bstream)
    bstream, session = _decode_deploy_executable_item(bstream)
    bstream, body_hash = decode_clv(CLT_ByteArray(32), bstream)

    return bstream, DeployBody(payment, session, body_hash.value)


def _decode_deploy_executable_item(bstream: bytes) -> DeployExecutableItem:
    if bstream[0] == 0:
        return decode(DeployOfModuleBytes, bstream)
    elif bstream[0] == 1:
        return decode(DeployOfStoredContractByHash, bstream)
    elif bstream[0] == 2:
        return decode(DeployOfStoredContractByHashVersioned, bstream)
    elif bstream[0] == 3:
        return decode(DeployOfStoredContractByName, bstream)
    elif bstream[0] == 4:
        return decode(DeployOfStoredContractByNameVersioned, bstream)
    elif bstream[0] == 5:
        return decode(DeployOfTransfer, bstream)

    raise ValueError("Invalid deploy executable item type tag")


def _decode_deploy_header(bstream: bytes) -> typing.Tuple[bytes, DeployHeader]:
    bstream, account = decode_clv(
        CLT_PublicKey(), bstream
        )
    bstream, timestamp = decode(Timestamp, bstream)
    bstream, ttl = decode(DeployTimeToLive, bstream)
    bstream, gas_price = decode_clv(CLT_U64(), bstream)
    bstream, body_hash = decode_clv(CLT_ByteArray(32), bstream)
    bstream, dependencies = decode_clv(
        CLT_List(CLT_ByteArray(32)), bstream
        )
    bstream, chain_name = decode_clv(CLT_String(), bstream)

    return bstream, DeployHeader(
        account=account,
        body_hash=body_hash.value,
        chain_name=chain_name.value,
        dependencies=dependencies.vector,
        gas_price=gas_price.value,
        timestamp=timestamp,
        ttl=ttl
    )


def _decode_deploy_time_to_live(bstream: bytes) -> typing.Tuple[bytes, DeployTimeToLive]:
    bstream, ttl = decode_clv(CLT_U64(), bstream)

    return bstream, DeployTimeToLive(
        ttl.value,
        convertor.humanized_time_interval_from_ms(ttl.value)
        )


def _decode_module_bytes(bstream: bytes) -> typing.Tuple[bytes, DeployOfModuleBytes]:
    bstream = bstream[1:]
    bstream, length = decode_clv(CLT_U32(), bstream)
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
    bstream, contract_hash = decode_clv(CLT_ByteArray(32), bstream)
    bstream, entry_point = decode_clv(CLT_String(), bstream)
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
    bstream, contract_hash = decode_clv(CLT_ByteArray(32), bstream)
    bstream, contract_version = decode_clv(CLT_U32(), bstream)
    bstream, entry_point = decode_clv(CLT_String(), bstream)
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
    bstream, contract_name = decode_clv(CLT_String(), bstream)
    bstream, entry_point = decode_clv(CLT_String(), bstream)
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
    bstream, contract_name = decode_clv(CLT_String(), bstream)
    bstream, contract_version = decode_clv(CLT_U32(), bstream)
    bstream, entry_point = decode_clv(CLT_String(), bstream)
    bstream, args = _decode_deploy_argument_set(bstream)

    return bstream, DeployOfStoredContractByNameVersioned(
        args=args,
        entry_point=entry_point.value,
        name=contract_name.value,
        version=contract_version.value
        )


def _decode_timestamp(bstream: bytes) -> typing.Tuple[bytes, Timestamp]:
    bstream, ts_ns = decode_clv(CLT_U64(), bstream)

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
