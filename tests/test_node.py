import bukkit


def test_creation():
    obj = object()
    node = bukkit.Node(obj)
    assert node.obj is obj, "Node object not assigned properly."
    assert node.prev_node is None
    assert node.next_node is None


def test_insert():
    first = bukkit.Node(None)
    second = bukkit.Node(None)
    second.insert_before(first)
    assert first.next_node is None
    assert first.prev_node is second
    assert second.next_node is first
    assert second.prev_node is None
