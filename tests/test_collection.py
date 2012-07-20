from bukkit import Collection


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
