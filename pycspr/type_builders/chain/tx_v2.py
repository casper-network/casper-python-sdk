from pycspr.type_builders.primitives import Timestamp_Builder
from pycspr.type_defs.chain import \
    Motes, \
    PricingMode, \
    TransactionBodyHash, \
    TransactionHash, \
    TransactionInitiatorAddress, \
    Transaction_V2 as Transaction, \
    Transaction_V2_Header as Header
from pycspr.type_defs.primitives import TimeDifference, Timestamp


class HeaderBuilder():
    def __init__(self):
        self.chain_name = None
        self.timestamp = Timestamp_Builder().build()
        self.ttl = None
        self.body_hash = None
        self.pricing_mode = None
        self.initiator_address = None

    def set_body_hash(self, value: TransactionBodyHash) -> "HeaderBuilder":
        assert isinstance(value, bytes) and len(value) == 32
        self.body_hash = value
        return self

    def set_chain_name(self, value: str) -> "HeaderBuilder":
        assert isinstance(value, str) and len(value) > 0
        self.chain_name = value
        return self

    def set_initiator_address(self, value: TransactionInitiatorAddress) -> "HeaderBuilder":
        self.initiator_address = value
        return self

    def set_pricing_mode(self, value: PricingMode) -> "HeaderBuilder":
        assert isinstance(value, PricingMode)
        self.pricing_mode = value
        return self

    def set_timestamp(self, value: Timestamp) -> "HeaderBuilder":
        assert isinstance(value, Timestamp)
        self.timestamp = value
        return self

    def set_ttl(self, value: TimeDifference) -> "HeaderBuilder":
        assert isinstance(value, TimeDifference)
        self.ttl = value
        return self

    def build(self) -> Header:
        return Header(
            body_hash=self.body_hash,
            chain_name=self.chain_name,
            initiator_address=self.initiator_address,
            timestamp=self.timestamp,
            ttl=self.ttl,
        )
