import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.chain.complex import \
    BlockHeader, \
    BlockHeader_V1, \
    BlockHeader_V2, \
    EraEnd, \
    EraEnd_V1, \
    EraEnd_V2, \
    ProtocolVersion
from pycspr.api.node.bin.types.chain.simple import \
    BlockBodyHash, \
    BlockHash, \
    BlockHeight, \
    EraID, \
    GasPrice
from pycspr.api.node.bin.types.primitives.crypto import DigestBytes, PublicKeyBytes
from pycspr.api.node.bin.types.primitives.numeric import U8, U32, U64
from pycspr.api.node.bin.types.primitives.time import Timestamp


def decode_block_header(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader]:
    bytes_rem, type_tag = decode(bytes_in, U8)
    if type_tag == 0:
        return decode_block_header_v1(bytes_rem)
    elif type_tag == 1:
        return decode_block_header_v2(bytes_rem)
    else:
        raise ValueError("Invalid type tag: block header ")


def decode_block_header_v1(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader_V1]:
    raise NotImplementedError()


def decode_block_header_v2(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader_V2]:
    print([i for i in bytes_in])

    bytes_rem, parent_block_hash = decode(bytes_in, BlockHash)
    bytes_rem, state_root_hash = decode(bytes_rem, DigestBytes)
    bytes_rem, body_hash = decode(bytes_rem, BlockBodyHash)
    bytes_rem, random_bit = decode(bytes_rem, bool)
    bytes_rem, accumulated_seed = decode(bytes_rem, DigestBytes)

    print([i for i in bytes_rem])
    print("-----")
    print("decoding era_end")
    bytes_rem, era_end = decode(bytes_rem, EraEnd_V2, is_optional=True)

    print("-----")
    print("decoding timestamp")
    bytes_rem, timestamp = decode(bytes_rem, Timestamp)

    print("-----")
    print("decoding era_id")
    bytes_rem, era_id = decode(bytes_rem, EraID)

    print("-----")
    print("decoding height")
    bytes_rem, height = decode(bytes_rem, BlockHeight)

    print("-----")
    print("decoding protocol_version")
    bytes_rem, protocol_version = decode(bytes_rem, ProtocolVersion)

    print("-----")
    print("decoding proposer")
    bytes_rem, proposer = decode(bytes_rem, PublicKeyBytes)

    print("-----")
    print("decoding current_gas_price")
    bytes_rem, current_gas_price = decode(bytes_rem, GasPrice)

    print("-----")
    print("decoding last_switch_block_hash")
    bytes_rem, last_switch_block_hash = decode(bytes_rem, DigestBytes)

    raise NotImplementedError()

    # self.parent_hash.write_bytes(writer)?;
    # self.state_root_hash.write_bytes(writer)?;
    # self.body_hash.write_bytes(writer)?;
    # self.random_bit.write_bytes(writer)?;
    # self.accumulated_seed.write_bytes(writer)?;
    # self.era_end.write_bytes(writer)?;
    # self.timestamp.write_bytes(writer)?;
    # self.era_id.write_bytes(writer)?;
    # self.height.write_bytes(writer)?;
    # self.protocol_version.write_bytes(writer)?;
    # self.proposer.write_bytes(writer)?;
    # self.current_gas_price.write_bytes(writer)?;
    # self.last_switch_block_hash.write_bytes(writer)



def decode_era_end_v1(bytes_in: bytes) -> typing.Tuple[bytes, EraEnd_V1]:

    raise NotImplementedError()


def decode_era_end_v2(bytes_in: bytes) -> typing.Tuple[bytes, EraEnd_V2]:

    raise NotImplementedError()


def decode_protocol_version(bytes_in: bytes) -> typing.Tuple[bytes, ProtocolVersion]:
    bytes_rem, major = decode(bytes_in, U32)
    bytes_rem, minor = decode(bytes_rem, U32)
    bytes_rem, patch = decode(bytes_rem, U32)

    return bytes_rem, ProtocolVersion(major, minor, patch)


register_decoders({
    (BlockBodyHash, lambda x: decode(x, DigestBytes)),
    (BlockHash, lambda x: decode(x, DigestBytes)),
    (BlockHeight, lambda x: decode(x, DigestBytes)),
    (BlockHeader, decode_block_header),
    (BlockHeader_V1, decode_block_header_v1),
    (BlockHeader_V2, decode_block_header_v2),
    (EraEnd_V1, decode_era_end_v1),
    (EraEnd_V2, decode_era_end_v2),
    (GasPrice, lambda x: decode(x, U8)),
    (ProtocolVersion, decode_protocol_version)
})
