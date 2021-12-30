import itertools
import typing

from pycspr.crypto.enums import HashAlgorithm
from pycspr.crypto.hashifier import get_hash


# The number of input bytes, at or below which [`encode`] will checksum-encode the output.
_SMALL_BYTES_COUNT: int = 75

# The set of characters to which nibbles will be mapped.
_HEX_CHARS: typing.List[str] = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f',
    'A', 'B', 'C', 'D', 'E', 'F',
]


def decode(input: str) -> bytes:
    """Maps input hexadecimal string to an array of bytes.

    :param input: A checksummed hexadecimal string to be mapped.
    :returns: An array of bytes.

    """
    input_bytes: bytes = bytes.fromhex(input)

    # Skip verification if the string was either large or single case.
    if len(input_bytes) > _SMALL_BYTES_COUNT or _is_string_same_case(input):
        return input_bytes

    # Verify checksum.
    for idx, (i, j) in enumerate(zip(input, _encode(input_bytes))):
        if i != j:
            raise ValueError(f"Checksum contains an invalid byte at position: {idx}")

    return input_bytes


def encode(input: bytes) -> str:
    """Encodes input bytes as hexadecimal with mixed-case based checksums
    following a scheme similar to [EIP-55][1].

    :param input: Input data to be encoded.
    :returns: Checksummed hexadecimal string.

    """
    # Return lower case for long inputs.
    if len(input) > _SMALL_BYTES_COUNT:
        return input.hex().lower()

    return "".join(_encode(input))


def encode_account_key(account_id: typing.Union[str, bytes]) -> str:
    """Encodes an account identifier as a checksummed hexadecimal string.

    :param block_id: An account identifier.
    :returns: Checksummed hexadecimal string.

    """
    if isinstance(account_id, str):
        account_id = bytes.fromhex(account_id)

    return account_id[:1].hex() + encode(account_id[1:])


def encode_block_id(block_id: typing.Union[str, bytes]) -> str:
    """Encodes a block identifier as a checksummed hexadecimal string.

    :param block_id: A block identifier.
    :returns: Checksummed hexadecimal string.

    """
    if isinstance(block_id, str):
        block_id = bytes.fromhex(block_id)

    return encode(block_id)


def encode_deploy_id(deploy_id: typing.Union[str, bytes]) -> str:
    """Encodes a deploy identifier as a checksummed hexadecimal string.

    :param deploy_id: A deploy identifier.
    :returns: Checksummed hexadecimal string.

    """
    if isinstance(deploy_id, str):
        deploy_id = bytes.fromhex(deploy_id)

    return encode(deploy_id)


def encode_digest(digest: typing.Union[str, bytes]) -> str:
    """Encodes a digest as a checksummed hexadecimal string.

    :param digest: A digest.
    :returns: Checksummed hexadecimal string.

    """
    if isinstance(digest, str):
        digest = bytes.fromhex(digest)

    return encode(digest)


def encode_signature(signature: typing.Union[str, bytes]) -> str:
    """Encodes a digital signature as a checksummed hexadecimal string.

    :param signature: A digital signature.
    :returns: Checksummed hexadecimal string.

    """
    if isinstance(signature, str):
        signature = bytes.fromhex(signature)

    return signature[:1].hex() + encode(signature[1:])


def _encode(input: bytes) -> typing.Iterator[str]:
    """Maps input to iterator of hexadecimal characters.

    """
    hash_bits: typing.Iterator[int] = _bytes_to_bits_cycle(
        get_hash(input, size=32, algo=HashAlgorithm.BLAKE2B)
    )
    for nibble in _bytes_to_nibbles(input):
        if nibble >= 10 and hash_bits.__next__() == 1:
            nibble += 6
        yield _HEX_CHARS[nibble]


def _bytes_to_bits_cycle(input: bytes) -> typing.Iterator[int]:
    """Maps input to a cyclic bit iterator.

    """
    def _iterator():
        for i in input:
            for offset in range(0, 8):
                yield (i >> offset) & 0x01

    return itertools.cycle(_iterator())


def _bytes_to_nibbles(input: typing.List[int]) -> typing.Iterator[int]:
    """Maps input to a iterator of nibbles.

    """
    for byte in input:
        for offset in [4, 0]:
            yield (byte >> offset) & 0x0F


def _is_string_same_case(input: str):
    """Returns flag indicating whether input string is a single case.

    """
    return input == input.lower() or input == input.upper()
