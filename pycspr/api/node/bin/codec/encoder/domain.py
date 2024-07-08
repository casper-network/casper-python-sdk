import typing

from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_bytes, \
    encode_u8, \
    encode_u64
from pycspr.api.node.bin.types.domain import \
    BlockHash, \
    BlockHeight, \
    BlockID, \
    ProtocolVersion


def encode_block_hash(val: BlockHash):
    return encode_u8(0) + encode_bytes(val)


def encode_block_height(val: BlockHeight):
    return encode_u8(1) + encode_u64(val)


def encode_block_id(val: BlockID):
    if isinstance(val, bytes):
        return encode_block_hash(val)
    elif isinstance(val, int):
        return encode_block_height(val)
    else:
        raise ValueError("Invalid BlockID")


def encode_protocol_version(entity: ProtocolVersion):
    return \
        encode_u8(entity.major) + \
        encode_u8(entity.minor) + \
        encode_u8(entity.patch),


ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    BlockHash: encode_block_hash,
    BlockHeight: encode_block_height,
    BlockID: encode_block_id,
    ProtocolVersion: encode_protocol_version,
}
