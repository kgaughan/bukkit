"""
Keyed collections of token buckets.
"""


import time
import weakref


__author__ = 'Keith Gaughan'
__email__ = 'k@stereochro.me'
__version__ = '0.1.0'


class TokenBucket(object):
    """
    A token bucket.
    """

    __slots__ = ('clock', 'ts', 'rate', 'limit', '_available')

    def __init__(self, rate, limit, clock=time.time):
        self.clock = clock
        self.ts = self.clock()
        self.rate = rate
        self.limit = limit
        self._available = limit

    def consume(self, tokens):
        """
        Attempt to remove the given number of tokens from this bucket. If
        there are enough tokens in the bucket to fulfil the request, we
        return `True`, otherwise `False`.
        """
        if 0 < tokens <= self.tokens:
            self._available -= tokens
            return True
        return False

    @property
    def tokens(self):
        """
        The number of tokens available in this bucket.
        """
        ts = self.clock()
        if self._available < self.limit:
            self._available += min(
                (ts - self.ts) * self.rate,
                self.limit - self._available)
        self.ts = ts
        return self._available

    def __cmp__(self, other):
        return cmp(self.ts, other.ts)


class Node(object):
    """Linked list node."""

    __slots__ = ('prev_node', 'obj', 'next_node')

    def __init__(self, obj):
        self.obj = obj
        self.prev_node = None
        self.next_node = None

    def detach(self):
        """
        Remove from the linked list and join the adjacent elements to one
        another.
        """
        self.prev_node.next_node = self.next_node
        self.next_node.prev_node = self.prev_node
        self.prev_node = None
        self.next_node = None

    def insert_before(self, other):
        """
        Insert this node before the `other`.
        """
        self.next_node = other
        self.prev_node = other.prev_node
        self.prev_node.next_node = self
        other.prev_node = self


class BucketCollection(object):
    """
    A keyed collection of token buckets.
    """

    __slots__ = (
        'head', 'tail', 'node_map',
        'rate', 'limit',
        'timeout',
        'clock')

    def __init__(self, rate, limit, timeout, clock=time.time):
        if timeout < limit:
            timeout = limit
        self.head_node = Node(None)
        self.tail_node = Node(None)
        self.head_node.prev_node = self.tail_node
        self.tail_node.next_node = self.head_node
        self.node_map = weakref.WeakValueDictionary()
        self.rate = rate
        self.limit = limit
        self.timeout = timeout
        self.clock = clock

    def __del__(self):
        node = self.tail_node.next_node
        while node is not self.head_node:
            next_node = node.next_node
            node.detach()
            del node
            node = next_node
        self.head_node.prev_node = None
        self.tail_node.next_node = None

    def __contains__(self, key):
        return key in self.node_map and self.node_map[key] is not None

    def __getitem__(self, key):
        if key in self.node_map:
            node = self.node_map[key]
            if node is not None:
                return node.obj
        raise IndexError("No such bucket: '%s'" % key)

    def _detach(self, key):
        """
        Detach the named token bucket from the collection for order cache
        order reassignment. It will also create a new token bucket if none
        match the name given in `key`.

        For internal use only."
        """
        if key in self.node_map:
            node = self.node_map[key]
        if node is None:
            node = Node(
                TokenBucket(
                    rate=self.rate, limit=self.limit, clock=self.clock))
            self.node_map[key] = node
        else:
            node.detach()
        return node

    def _move_to_head(self, node):
        """
        Attach the named token bucket at the head of the cache.
        """
        node.insert_before(self.head_node)

    def consume(self, key, tokens):
        """
        Attempt to consume the given number of token in the bucket identified
        by `key`. Returns `True` if succeeds, otherwise `False`.
        """
        node = self._detach(key)
        result = node.obj.consume(tokens)
        self._move_to_head(node)
        return result

    def purge(self):
        """
        Purge all expired buckets.
        """
        limit = self.clock() - self.timeout
        node = self.tail_node.next_node
        while node is not self.head_node and node.obj.ts <= limit:
            next_node = node.next_node
            node.detach()
            del node
            node = next_node
