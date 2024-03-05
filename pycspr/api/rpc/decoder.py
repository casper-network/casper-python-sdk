import typing

from pycspr.api.rpc.types import AuctionBidByDelegator
from pycspr.api.rpc.types import AuctionBidByValidator
from pycspr.api.rpc.types import AuctionBidByValidatorInfo
from pycspr.api.rpc.types import AuctionState
from pycspr.api.rpc.types import BlockTransfers
from pycspr.api.rpc.types import EraInfo
from pycspr.api.rpc.types import EraSummary
from pycspr.api.rpc.types import EraValidators
from pycspr.api.rpc.types import EraValidatorWeight
from pycspr.api.rpc.types import SeigniorageAllocation
from pycspr.api.rpc.types import SeigniorageAllocationForDelegator
from pycspr.api.rpc.types import SeigniorageAllocationForValidator
from pycspr.api.rpc.types import Transfer
from pycspr.api.rpc.types import URef
from pycspr.api.rpc.types import URefAccessRights
from pycspr.api.rpc.types import ValidatorChanges
from pycspr.api.rpc.types import ValidatorStatusChange
from pycspr.api.rpc.types import ValidatorStatusChangeType


def decode(typedef: type, encoded: dict) -> object:
    """Decodes a domain entity from a JSON object.

    :param obj: A JSON compatible dictionary.
    :param typedef: Domain entity type definition.
    :returns: A domain entity.

    """
    try:
        decoder = _DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from json object")
    else:
        return decoder(encoded)


def _decode_account_id(encoded: str) -> bytes:
    # E.G. account-hash-2c4a11c062a8a337bfc97e27fd66291caeb2c65865dcb5d3ef3759c4c97efecb
    return encoded[13:].encode("utf-8")


def _decode_auction_bid_by_delegator(encoded: dict) -> AuctionBidByDelegator:
    return AuctionBidByDelegator(
        bonding_purse=_decode_uref(encoded["bonding_purse"]),
        delegatee=_decode_public_key(encoded["delegatee"]),
        public_key=_decode_public_key(encoded["public_key"]),
        staked_amount=_decode_motes(encoded["staked_amount"]),
    )


def _decode_auction_bid_by_validator(encoded: dict) -> AuctionBidByValidator:
    return AuctionBidByValidator(
        public_key=_decode_public_key(encoded["public_key"]),
        bid=_decode_auction_bid_by_validator_info(encoded["bid"]),
    )


def _decode_auction_bid_by_validator_info(encoded: dict) -> AuctionBidByValidatorInfo:
    return AuctionBidByValidatorInfo(
        bonding_purse=_decode_uref(encoded["bonding_purse"]),
        delegation_rate=int(encoded["delegation_rate"]),
        delegators=_map(_decode_auction_bid_by_delegator, encoded["delegators"]),
        inactive=encoded["inactive"],
        staked_amount=_decode_motes(encoded["staked_amount"]),
    )


def _decode_auction_state(encoded: dict) -> AuctionState:
    return AuctionState(
        bids=_map(_decode_auction_bid_by_validator, encoded["bids"]),
        block_height=encoded["block_height"],
        # era_validators=_decode_era_validators(encoded["era_validators"]),
        era_validators=_map(_decode_era_validators, encoded["era_validators"]),
        state_root=_decode_state_root(encoded["state_root_hash"])
    )


def _decode_block_id(encoded: str) -> bytes:
    return encoded.encode("utf-8")


def _decode_block_transfers(encoded: dict) -> BlockTransfers:
    return BlockTransfers(
        block_hash=encoded["block_hash"].encode("utf-8"),
        transfers=_map(_decode_transfer, encoded["transfers"])
    )


def _decode_era_info(encoded: dict) -> EraInfo:
    return EraInfo(
        seigniorage_allocations=[
            _decode_seigniorage_allocation(i) for i in encoded["seigniorage_allocations"]
            ]
    )


def _decode_era_validators(encoded: dict) -> EraValidators:
    return EraValidators(
        era_id=encoded["era_id"],
        validator_weights=_map(_decode_era_validator_weight, encoded["validator_weights"])
    )


def _decode_era_validator_weight(encoded: dict) -> EraValidatorWeight:
    return EraValidatorWeight(
        public_key=_decode_public_key(encoded["public_key"]),
        weight=int(encoded["weight"])
    )


def _decode_era_summary(encoded: dict) -> EraSummary:
    return EraSummary(
        block_hash=_decode_block_id(encoded["block_hash"]),
        era_id=encoded["era_id"],
        era_info=_decode_era_info(encoded["stored_value"]["EraInfo"]),
        merkle_proof=_decode_merkle_proof(encoded["merkle_proof"]),
        state_root=_decode_state_root(encoded["state_root_hash"]),
    )


def _decode_merkle_proof(encoded: str) -> bytes:
    return bytes.fromhex(encoded)


def _decode_motes(encoded: str) -> int:
    return int(encoded)


def _decode_public_key(encoded: str) -> bytes:
    return bytes.fromhex(encoded)


def _decode_seigniorage_allocation(encoded: dict) -> SeigniorageAllocation:
    def decode_delegator_seigniorage_allocation(encoded: dict):
        return SeigniorageAllocationForDelegator(
            amount=_decode_motes(encoded["amount"]),
            delegator_public_key=_decode_public_key(encoded["delegator_public_key"]),
            validator_public_key=_decode_public_key(encoded["validator_public_key"]),
        )

    def decode_validator_seigniorage_allocation(encoded: dict):
        return SeigniorageAllocationForValidator(
            amount=_decode_motes(encoded["amount"]),
            validator_public_key=_decode_public_key(encoded["validator_public_key"]),
        )

    if "Delegator" in encoded:
        return decode_delegator_seigniorage_allocation(encoded["Delegator"])
    elif "Validator" in encoded:
        return decode_validator_seigniorage_allocation(encoded["Validator"])
    else:
        raise ValueError("decode_seigniorage_allocation")


def _decode_state_root(encoded: str) -> bytes:
    return bytes.fromhex(encoded)


def _decode_stored_value(encoded: dict) -> typing.Union[EraInfo]:
    if "EraInfo" in encoded:
        _decode_era_info(encoded["EraInfo"])


def _decode_transfer(encoded: dict) -> Transfer:
    return Transfer(
        amount=_decode_motes(encoded["amount"]),
        deploy_hash=bytes.fromhex(encoded["deploy_hash"]),
        from_=_decode_account_id(encoded["from"]),
        gas=int(encoded["gas"]),
        source=_decode_uref(encoded["source"]),
        target=_decode_uref(encoded["target"]),
        correlation_id=int(encoded["id"]),
        to_=_decode_account_id(encoded["to"]),
    )


def _decode_uref(encoded: str) -> URef:
    # E.G. uref-bc4f1cd8cbb7a47464ea82e5dbd045c99f6c2fabedd54df1f50b08fbb9ed35ca-007.
    return URef(
        access_rights=URefAccessRights(int(encoded[-3:])),
        address=bytes.fromhex(encoded[5:-4])
    )


def _decode_validator_changes(encoded: list) -> typing.List[ValidatorChanges]:
    def _decode_status_change(encoded: dict) -> ValidatorStatusChange:
        return ValidatorStatusChange(
            era_id=int(encoded["era_id"]),
            status_change=ValidatorStatusChangeType[encoded["validator_change"]]
        )

    def _decode_changes(encoded: dict) -> ValidatorChanges:
        return ValidatorChanges(
            public_key=_decode_public_key(encoded["public_key"]),
            status_changes=_map(_decode_status_change, encoded["status_changes"])
        )

    return _map(_decode_changes, encoded)


_DECODERS = {
    AuctionState: _decode_auction_state,
    BlockTransfers: _decode_block_transfers,
    EraSummary: _decode_era_summary,
    ValidatorChanges: _decode_validator_changes
}


def _map(func, data) -> list:
    return [func(i) for i in data]
