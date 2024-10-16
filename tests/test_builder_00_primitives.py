from pycspr.api.node.bin.builders import primitives as builders
from pycspr.type_defs.primitives import TimeDifference, Timestamp
from tests.utils import assert_entity


async def test_build_time_difference():
    assert_entity(
        builders.TimeDifference_Builder()
            .set_delta(int(1e9))
            .build(),
        TimeDifference
    )


async def test_build_timestamp():
    assert_entity(
        builders.Timestamp_Builder()
            .set_ts(1e9)
            .build(),
        Timestamp
    )
