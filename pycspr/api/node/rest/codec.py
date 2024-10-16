from pycspr.api.node.rest.type_defs import \
    MinimalBlockInfo, \
    NextUpgradeInfo, \
    NodePeer, \
    NodeStatus, \
    ReactorState, \
    ValidatorChanges, \
    ValidatorStatusChangeType
from pycspr.type_defs.chain import \
    AvailableBlockRange as BlockRange, \
    BlockHash, \
    BlockHeight, \
    EraID, \
    StateRootHash
from pycspr.type_defs.primitives import Timestamp
from pycspr.serializer.json.decoder_crypto import DECODERS as CRYPTO_DECODERS
from pycspr.serializer.json.decoder_primitives import DECODERS as PRIMITIVES_DECODERS
from pycspr.type_defs.crypto import DigestHex, PublicKey, PublicKeyHex
from pycspr.utils import convertor


def decode(encoded: object, typedef: object) -> object:
    """Decodes a domain type instance from JSON encoded type instance.

    :param typedef: Domain type to be instantiated.
    :param encoded: JSON encoded type instance.
    :returns: Domain type instance.

    """
    try:
        decoder = DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from json")
    else:
        return decoder(encoded)


def _decode_block_range(encoded: dict) -> BlockRange:
    return BlockRange(
        low=encoded["low"],
        high=encoded["high"]
    )


def _decode_minimal_block_info(encoded: dict) -> MinimalBlockInfo:
    return MinimalBlockInfo(
        creator=decode(encoded["creator"], PublicKeyHex),
        era_id=decode(encoded["era_id"], EraID),
        hash=decode(encoded["hash"], BlockHash),
        height=decode(encoded["height"], BlockHeight),
        state_root_hash=decode(encoded["state_root_hash"], StateRootHash),
        timestamp=decode(encoded["timestamp"], Timestamp),
    )


def _decode_next_upgrade_info(encoded: dict) -> NextUpgradeInfo:
    if encoded is not None:
        return NextUpgradeInfo(
            activation_point=decode(encoded["activation_point"], str),
            protocol_version=decode(encoded["protocol_version"], str),
        )


def _decode_node_peer(encoded: dict) -> NodePeer:
    return NodePeer(
        address=decode(encoded["address"], str),
        node_id=decode(encoded["node_id"], str),
    )


def _decode_node_status(encoded: dict) -> NodeStatus:
    # TODO: decode round length -> time duration
    return NodeStatus(
        api_version=decode(encoded["api_version"], str),
        available_block_range=decode(encoded["available_block_range"], BlockRange),
        build_version=decode(encoded["build_version"], str),
        chainspec_name=decode(encoded["chainspec_name"], str),
        last_added_block_info=decode(encoded["last_added_block_info"], MinimalBlockInfo),
        latest_switch_block_hash=decode(encoded["latest_switch_block_hash"], BlockHash),
        last_progress=decode(encoded["last_progress"], Timestamp),
        next_upgrade=decode(encoded["next_upgrade"], NextUpgradeInfo),
        our_public_signing_key=decode(encoded["our_public_signing_key"], PublicKeyHex),
        peers=[decode(i, NodePeer) for i in encoded["peers"]],
        reactor_state=decode(encoded["reactor_state"], ReactorState),
        round_length=decode(encoded["round_length"], str),
        starting_state_root_hash=decode(encoded["starting_state_root_hash"], StateRootHash),
        uptime=decode(encoded["uptime"], str),
    )


def _decode_timestamp(encoded: str) -> Timestamp:
    return Timestamp(convertor.timestamp_from_iso_datetime(encoded))


def _decode_validator_changes(encoded: list) -> ValidatorChanges:
    return ValidatorChanges(
        public_key=decode(PublicKeyHex, encoded["public_key"]),
        status_changes=[decode(ValidatorStatusChange, i) for i in encoded["status_changes"]],
    )


DECODERS = PRIMITIVES_DECODERS | CRYPTO_DECODERS | {
    BlockHash: lambda x: decode(x, DigestHex),
    BlockHeight: lambda x: decode(x, int),
    EraID: lambda x: decode(x, int),
    ReactorState: lambda x: ReactorState(x),
    StateRootHash: lambda x: decode(x, DigestHex),
    ValidatorStatusChangeType: lambda x: ValidatorStatusChangeType(x),
} | {
    BlockRange: _decode_block_range,
    MinimalBlockInfo: _decode_minimal_block_info,
    NextUpgradeInfo: _decode_next_upgrade_info,
    NodePeer: _decode_node_peer,
    NodeStatus: _decode_node_status,
    Timestamp: _decode_timestamp,
    ValidatorChanges: _decode_validator_changes,
}
