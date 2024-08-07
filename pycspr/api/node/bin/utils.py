import typing

# Set of codec tags.
TAG_DOMAIN_BLOCK_HASH: int = 0
TAG_DOMAIN_BLOCK_HEIGHT: int = 1
TAG_EP_GET: int = 0
TAG_EP_GET_INFORMATION: int = 1
TAG_EP_GET_INFORMATION_AVAILABLE_BLOCK_RANGE: int = 10
TAG_EP_GET_INFORMATION_BLOCK_HEADER: int = 0
TAG_EP_GET_INFORMATION_BLOCK_SYNCHRONIZER_STATUS: int = 9
TAG_EP_GET_INFORMATION_CHAINSPEC_RAW_BYTES: int = 13
TAG_EP_GET_INFORMATION_CONSENSUS_STATUS: int = 12
TAG_EP_GET_INFORMATION_CONSENSUS_VALIDATOR_CHANGES: int = 8
TAG_EP_GET_INFORMATION_LAST_PROGRESS: int = 5
TAG_EP_GET_INFORMATION_LATEST_SWITCH_BLOCK_HEADER: int = 15
TAG_EP_GET_INFORMATION_NETWORK_NAME: int = 7
TAG_EP_GET_INFORMATION_NEXT_UPGRADE: int = 11
TAG_EP_GET_INFORMATION_NODE_STATUS: int = 14
TAG_EP_GET_INFORMATION_PEERS: int = 3
TAG_EP_GET_INFORMATION_REACTOR_STATE: int = 6
TAG_EP_GET_INFORMATION_REWARD: int = 16
TAG_EP_GET_INFORMATION_SIGNED_BLOCK: int = 1
TAG_EP_GET_INFORMATION_TRANSACTION: int = 2
TAG_EP_GET_INFORMATION_UPTIME: int = 4
TAG_EP_GET_RECORD: int = 0
TAG_EP_GET_STATE: int = 2
TAG_EP_TRY_ACCEPT_TRANSACTION: int = 1
TAG_EP_TRY_SPECULATIVE_TRANSACTION: int = 2
TAG_OPTIONAL_NONE: int = 0
TAG_OPTIONAL_VALUE: int = 1


def decode_optional(
    bytes_in: bytes,
    decoder: typing.Callable
) -> typing.Tuple[bytes, typing.Optional[object]]:
    bytes_rem, flag = decode_u8(bytes_in)
    if flag == 0:
        return bytes_rem, None
    else:
        return decoder(bytes_rem)


def decode_u8(bytes_in: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bytes_in, 1)


def decode_u16(bytes_in: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bytes_in, 2)


def decode_u32(bytes_in: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bytes_in, 4)


def decode_u64(bytes_in: bytes) -> typing.Tuple[bytes, int]:
    print(bytes_in)
    return decode_uint(bytes_in, 8)


def decode_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


def encode_bytes(entity: bytes) -> bytes:
    return encode_u32(len(entity)) + entity


def encode_optional(entity: object, encoder: typing.Callable) -> bytes:
    if entity is None:
        return encode_u8(TAG_OPTIONAL_NONE)
    else:
        return encode_u8(TAG_OPTIONAL_VALUE) + encoder(entity)


def encode_u8(entity: int) -> bytes:
    return encode_uint(entity, 1)


def encode_u16(entity: int) -> bytes:
    return encode_uint(entity, 2)


def encode_u32(entity: int) -> bytes:
    return encode_uint(entity, 4)


def encode_u64(entity: int) -> bytes:
    return encode_uint(entity, 8)


def encode_uint(entity: int, encoded_length: int) -> bytes:
    return entity.to_bytes(encoded_length, "little", signed=False)
