from bukkit import Node
import cPickle as pickle


def test_creation():
    obj = object()
    node = Node(obj)
    assert node.obj is obj, "Node object not assigned properly."
    assert node.prev_node is None
    assert node.next_node is None


def test_insert():
    # Insert at tail.
    first = Node(None)
    second = Node(None)
    second.insert_after(first)
    assert first.next_node is None
    assert first.prev_node is second
    assert second.next_node is first
    assert second.prev_node is None

    # Insert between two nodes.
    third = Node(None)
    third.insert_after(first)
    assert first.prev_node is third
    assert second.next_node is third
    assert third.prev_node is second
    assert third.next_node is first


def test_from_list_and_iter():
    assert Node.from_list([]) is None
    for lst in ([1], [1, 2], [1, 2, 3]):
        assert lst == list(Node.from_list(lst))


def test_detach_tail():
    first = Node(None)
    second = Node(None)
    third = Node(None)
    second.insert_after(first)
    third.insert_after(second)
    third.detach()
    assert first.next_node is None
    assert first.prev_node is second
    assert second.next_node is first
    assert second.prev_node is None
    assert third.next_node is None
    assert third.prev_node is None


def test_detach_middle():
    first = Node(None)
    second = Node(None)
    third = Node(None)
    second.insert_after(first)
    third.insert_after(second)
    second.detach()
    assert first.prev_node is third
    assert third.next_node is first
    assert second.prev_node is None
    assert second.next_node is None
