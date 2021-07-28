import random

import pycspr



def test_that_humanized_time_interval_can_be_converted_to_milliseconds():
    convertor = pycspr.utils.conversion.humanized_time_interval_to_milliseconds
    for (unit, ms, quantity) in (
        ("ms", 1, random.randint(1, 1e9)),
        ("s", 1000, random.randint(1, 60)),
        ("m", 60000, random.randint(1, 60)),
        ("h", 3600000, random.randint(1, 24)),
        ("day", 86400000, random.randint(1, 366))
    ):
        assert convertor(f"{quantity}{unit}") == quantity * ms
