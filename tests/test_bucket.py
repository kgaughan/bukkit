import bukkit
import time


def test_creation():
    ticks = 42
    fake_clock = lambda: ticks

    bucket = bukkit.TokenBucket(rate=23, limit=9000, clock=fake_clock)
    assert bucket.clock is fake_clock
    assert bucket.ts == ticks
    assert bucket.rate == 23
    assert bucket.limit == 9000
    assert bucket._available == bucket.limit
