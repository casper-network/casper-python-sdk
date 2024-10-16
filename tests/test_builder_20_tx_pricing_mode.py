from pycspr.api.node.bin.builders import chain as builders
from pycspr.type_defs.chain import PricingMode
from tests.utils import assert_entity, test_data_generator as tdgen


async def test_build_classic():
    assert_entity(
        builders.PricingMode_Builder.classic()
            .set_gas_price_tolerance(3)
            .set_payment_amount(int(1e9))
            .set_standard_payment_flag(True)
            .build(),
        PricingMode
    )


async def test_build_fixed():
    assert_entity(
        builders.PricingMode_Builder.fixed()
            .set_gas_price_tolerance(3)
            .build(),
        PricingMode
    )


async def test_build_reserved():
    assert_entity(
        builders.PricingMode_Builder.reserved()
            .set_receipt(
                tdgen.get_digest()
            )
            .build(),
        PricingMode
    )
