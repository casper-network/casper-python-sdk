import random

from pycspr.api.node.bin.builders.chain.tx_v2 import HeaderBuilder
from pycspr.type_builders.primitives import TimeDifference_Builder, Timestamp_Builder
from pycspr.type_defs.chain import Transaction_V2_Header as Tx_Header
from tests.utils import test_data_generator as tdgen


async def test_build_tx_v2_header():
    builder = HeaderBuilder()
    builder.set_body_hash(
        tdgen.get_digest()
    )
    builder.set_chain_name(
        tdgen.get_chain_name()
    )
    builder.set_initiator_address(
        tdgen.get_chain_name()
    )
    # builder.set_pricing_mode(
    #     tdgen.get_chain_name()
    # )
    builder.set_timestamp(
        Timestamp_Builder().set_ts(
            float(tdgen.get_timestamp_posix())
        ).build()
    )
    builder.set_ttl(
        TimeDifference_Builder().set_delta(
            tdgen.get_timestamp_posix()
        ).build()
    )

    assert isinstance(builder.build(), Tx_Header)
