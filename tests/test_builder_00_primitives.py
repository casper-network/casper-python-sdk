import pycspr.type_builders.primitives as builders
import pycspr.type_defs.primitives as types
from tests.utils import assert_entity


async def test_build_time_difference():
    assert_entity(
        builders.TimeDifference_Builder()
            .set_delta(int(1e9))
            .build(),
        types.TimeDifference
    )


async def test_build_timestamp():
    assert_entity(
        builders.Timestamp_Builder()
            .set_ts(1e9)
            .build(),
        types.Timestamp
    )
