import random

from pycspr.utils import convertor


def test_ms_from_humanized_time_interval():
    for (unit, ms, quantity) in (
        ("ms", 1, random.randint(1, int(1e9))),
        ("s", 1000, random.randint(1, 60)),
        ("m", 60000, random.randint(1, 60)),
        ("h", 3600000, random.randint(1, 2)),
    ):
        assert convertor.ms_from_humanized_time_interval(f"{quantity}{unit}") == quantity * ms
