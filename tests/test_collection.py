from bukkit import Collection
import cPickle as pickle


def test_creation():
    buckets = Collection(rate=5, limit=23, timeout=31, clock=lambda: 0)
    assert buckets.rate == 5
    assert buckets.limit == 23
    assert buckets.timeout == 31
    assert buckets.head_node.prev_node is buckets.tail_node
    assert buckets.tail_node.next_node is buckets.head_node


def test_consume():
    buckets = Collection(rate=5, limit=23, timeout=31, clock=lambda: 0)
    # Consuming nothing ensures the thing is present.
    buckets.consume('thingy', 0)
    assert buckets['thingy'].tokens == 23
    buckets.consume('thingy', 3)
    assert buckets['thingy'].tokens == 20


def test_contains():
    buckets = Collection(rate=5, limit=23, timeout=31, clock=lambda: 0)

    assert len(buckets.node_map) == 0
    assert 'thingy' not in buckets
    buckets.consume('thingy', 5)
    assert len(buckets.node_map) == 1
    assert 'thingy' in buckets


def test_get():
    buckets = Collection(rate=5, limit=23, timeout=31, clock=lambda: 0)

    try:
        buckets['thingy']
        assert False, "Should not be able to look up 'thingy'"
    except IndexError, exc:
        assert str(exc) == "No such bucket: 'thingy'"

    buckets.consume('thingy', 5)
    assert buckets['thingy'].tokens == 18


def test_purge():
    ticks = 0
    fake_clock = lambda: ticks
    buckets = Collection(rate=1, limit=20, timeout=15, clock=fake_clock)

    # Create a bunch of buckets for messing with.
    for i in xrange(4):
        buckets.consume('x' + str(i), 0)
    assert sorted(buckets.node_map.keys()) == ['x0', 'x1', 'x2', 'x3']

    ticks += 5
    buckets.consume('x1', 0)
    assert buckets['x1'].ts == ticks
    buckets.purge()
    assert len(buckets.node_map) == 4

    ticks += 5
    buckets.consume('x2', 0)
    assert buckets['x2'].ts == ticks
    buckets.purge()
    assert len(buckets.node_map) == 4

    ticks += 5
    buckets.consume('x3', 0)
    assert buckets['x3'].ts == ticks
    buckets.purge()
    assert len(buckets.node_map) == 3

    ticks += 5
    buckets.purge()
    assert len(buckets.node_map) == 2

    ticks += 5
    buckets.purge()
    assert len(buckets.node_map) == 1

    ticks += 5
    buckets.purge()
    assert len(buckets.node_map) == 0


def test_pickle():
    buckets = Collection(rate=3, limit=23, timeout=13)
    buckets.consume('x1', 1)
    buckets.consume('x2', 2)

    unpickled = pickle.loads(pickle.dumps(buckets))

    for attr in ('rate', 'limit', 'timeout'):
        assert getattr(buckets, attr) == getattr(unpickled, attr)
    assert buckets.clock is unpickled.clock

    # Working under the assumption currently that if node_map's keys were
    # populated properly and if the node chains are the same length, that
    # everything was unpickled properly.
    assert sorted(buckets.node_map.keys()) == sorted(unpickled.node_map.keys())
    assert len(list(buckets.head_node)) == len(list(unpickled.head_node))
