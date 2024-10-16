from pycspr.type_builders.builders.chain.accounts import AccountAddress_Builder
from pycspr.type_defs.chain import \
    Motes, \
    PricingMode_Classic, \
    PricingMode_Fixed, \
    PricingMode_Reserved
from pycspr.type_defs.crypto import \
    DigestBytes, \
    KeyAlgorithm, \
    PublicKey, \
    PublicKeyBytes
from pycspr.utils.constants import DEFAULT_TX_GAS_PRICE_TOLERANCE


class InitiatorAddress_Builder():
    """Factory: Tx initiator address.

    """
    class AccountHash_Builder():
        def __init__(self):
            self.account_hash = None

        def set_account_hash(self):
            self.account_hash = value
            return self

        def build(self) -> DigestBytes:
            raise NotImplementedError()

    class PublicKey_Builder():
        def __init__(self):
            self.account_hash = None

        def set_algo(self, value: KeyAlgorithm):
            assert isinstance(value, KeyAlgorithm)
            self.algo = value
            return self

        def set_key(self, value: PublicKeyBytes):
            assert isinstance(value, bytes) and len(value) in (32, 33)
            self.algo = value
            return self


        def build(self) -> PublicKey:
            raise NotImplementedError()

    @staticmethod
    def account_hash() -> "AccountHash_Builder":
        return AccountHash_Builder()

    @staticmethod
    def public_key() -> "PublicKey_Builder":
        return PublicKey_Builder()


class PricingMode_Builder():
    """Builder: Tx pricing mode.

    """
    class Classic_Builder():
        """Builder: Tx pricing mode -> classic.

        """
        def __init__(self):
            self.gas_price_tolerance = DEFAULT_TX_GAS_PRICE_TOLERANCE
            self.payment_amount = None
            self.standard_payment = True

        def set_gas_price_tolerance(self, value: int) -> "PricingMode_Classic_Builder":
            assert isinstance(value, int) and (0 < value < 5)
            self.gas_price_tolerance = value
            return self

        def set_payment_amount(self, value: Motes) -> "PricingMode_Classic_Builder":
            assert isinstance(value, int) and (0 < value < int(1e18))
            self.payment_amount = value
            return self

        def set_standard_payment_flag(self, value: bool) -> "PricingMode_Classic_Builder":
            assert isinstance(value, bool)
            self.standard_payment = value
            return self

        def build(self) -> "PricingMode_Classic_Builder":
            return PricingMode_Classic(
                gas_price_tolerance=self.gas_price_tolerance,
                payment_amount=self.payment_amount,
                standard_payment=self.set_standard_payment_flag,
            )

    class Fixed_Builder():
        """Builder: Tx pricing mode -> fixed.

        """
        def __init__(self):
            self.gas_price_tolerance = DEFAULT_TX_GAS_PRICE_TOLERANCE

        def set_gas_price_tolerance(self, value: int) -> "PricingMode_Fixed_Builder":
            assert isinstance(value, int) and (0 < value < 5)
            self.gas_price_tolerance = value
            return self

        def build(self) -> "PricingMode_Fixed_Builder":
            return PricingMode_Fixed(
                gas_price_tolerance=self.gas_price_tolerance,
            )

    class Reserved_Builder():
        """Builder: Tx pricing mode -> reserved.

        """
        def __init__(self):
            self.receipt = None

        def set_receipt(self, value: DigestBytes) -> "PricingMode_ReservedBuilder":
            self.receipt = value
            return self

        def build(self) -> "PricingMode_ReservedBuilder":
            return PricingMode_Reserved(
                receipt=self.receipt,
            )

    @staticmethod
    def classic() -> "Classic_Builder":
        return PricingMode_Builder.Classic_Builder()

    @staticmethod
    def fixed() -> "Fixed_Builder":
        return PricingMode_Builder.Fixed_Builder()

    @staticmethod
    def reserved() -> "PricingMode_ReservedBuilder":
        return PricingMode_Builder.Reserved_Builder()
