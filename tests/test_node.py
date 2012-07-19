import bukkit


def test_creation():
    obj = object()
    node = bukkit.Node(obj)
    assert node.obj is obj, "Node object not assigned properly."
    assert node.prev_node is None
    assert node.next_node is None


def test_insert():
    # Insert at tail.
    first = bukkit.Node(None)
    second = bukkit.Node(None)
    second.insert_before(first)
    assert first.next_node is None
    assert first.prev_node is second
    assert second.next_node is first
    assert second.prev_node is None

    # Insert between two nodes.
    third = bukkit.Node(None)
    third.insert_before(first)
    assert first.prev_node is third
    assert second.next_node is third
    assert third.prev_node is second
    assert third.next_node is first


def test_detach_tail():
    first = bukkit.Node(None)
    second = bukkit.Node(None)
    third = bukkit.Node(None)
    second.insert_before(first)
    third.insert_before(second)
    third.detach()
    assert first.next_node is None
    assert first.prev_node is second
    assert second.next_node is first
    assert second.prev_node is None
    assert third.next_node is None
    assert third.prev_node is None

def test_detach_middle():
    first = bukkit.Node(None)
    second = bukkit.Node(None)
    third = bukkit.Node(None)
    second.insert_before(first)
    third.insert_before(second)
    second.detach()
    assert first.prev_node is third
    assert third.next_node is first
    assert second.prev_node is None
    assert second.next_node is None
