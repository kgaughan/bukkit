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


def test_consumption():
    ticks = 0
    fake_clock = lambda: ticks

    bucket = bukkit.TokenBucket(5, 20, clock=fake_clock)
    assert bucket.tokens == 20
    assert bucket.consume(10)
    assert not bucket.consume(15)
    assert bucket.tokens == 10
    
    ticks += 1
    assert bucket.tokens == 15
    ticks += 2
    assert bucket.tokens == 20

    assert bucket.consume(1)
    assert bucket.tokens == 19
    ticks += 1
    assert bucket.tokens == 20
