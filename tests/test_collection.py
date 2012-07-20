from bukkit import Collection


def test_creation():
    buckets = Collection(rate=5, limit=23, timeout=31, clock=lambda: 0)
    assert buckets.rate == 5
    assert buckets.limit == 23
    assert buckets.timeout == 31
    assert buckets.head_node.prev_node is buckets.tail_node
    assert buckets.tail_node.next_node is buckets.head_node
