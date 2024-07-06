import typing

from pycspr.api.node.bin import types


ENCODERS: typing.Dict[typing.Type, typing.Callable] = \
{
    types.domain.BlockHash: \
        lambda x:\
            encode_u8(0) + \
            encode_bytes(x),

    types.domain.BlockHeight: \
        lambda x:\
            encode_u8(1) + \
            encode_u64(x),

    types.domain.ProtocolVersion: \
        lambda x:\
            encode_u8(x.major) + \
            encode_u8(x.minor) + \
            encode_u8(x.patch),
} | {
    types.request.get.information.GetBlockHeaderRequest: \
        lambda x:\
            encode(types.request.core.RequestType_Get_Information.BlockHeader) + \
            encode_optional(x.block_id, encode_block_id)
} | {
    types.request.core.Request: \
        lambda x:\
            encode(x.header) + \
            encode(x.body),

    types.request.core.RequestHeader: \
        lambda x:\
            encode_u16(x.binary_request_version) + \
            encode(x.chain_protocol_version) + \
            encode(x.type_tag) + \
            encode_u16(x.id),

    types.request.core.RequestType: \
        lambda x:\
            encode_u8(x.value),

    types.request.core.RequestType_Get: \
        lambda x:\
            encode_u8(x.value),

    types.request.core.RequestType_Get_Information: \
        lambda x:\
            encode(types.request.core.RequestType_Get.Information) + \
            encode_u8(x.value),
}

def encode(entity: object) -> bytes:
    try:
        encoder = ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"Unencodeable type: {type(entity)}")
    else:
        return encoder(entity)


def encode_block_id(val: types.domain.BlockID):
    if isinstance(val, bytes):
        return encode_u8(0) + encode_bytes(val)
    elif isinstance(val, int):
        return encode_u8(1) + encode_u64(val)
    else:
        raise ValueError("Invalid BlockID")


def encode_bytes(val: bytes):
    return encode_u32(len(val)) + val


def encode_optional(val: object, encoder = None):
    if val is None:
        return encode_u8(0)
    else:
        return encode_u8(1) + encode(val) if encoder is None else encoder(val)


def encode_u8(val: int):
    return encode_uint(val, 1)


def encode_u16(val: int):
    return encode_uint(val, 2)


def encode_u32(val: int):
    return encode_uint(val, 4)


def encode_u64(val: int):
    return encode_uint(val, 8)


def encode_uint(val: int, encoded_length: int):
    return val.to_bytes(encoded_length, "little", signed=False)
