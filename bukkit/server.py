"""
Simple network interface for managing a set of token bucket collections.

Protocol
~~~~~~~~

Responses are terminated by double-linefeeds. In the descriptions, semicolons
are used to represent linefeeds for compactness.  Field order within requests
can vary, but the command line must always come first. Responses follow the
same format as requests.

Request format:

  B;r=<rate>;l=<limit>;t=<timeout>;c=<collection>
    - Create a bucket collection with the given settings. Always responds
      with '+'. Note that if a collection already exists with the given name,
      it will be destroyed.
  C;c=<collection>;b=<bucket>;t=<tokens>
    - Attempt to consume the given tokens from the named bucket in the named
      collection. Response is '+'if successful, '-' if not.

  If the response code starts with '!', an error message follows in the 'm'
  attribute.
"""

import asynchat
import asyncore
import socket

from bukkit import bucket


_REQS = {
    # Create bucket:
    # B;r=<rate>;l=<limit>;t=<timeout>;c=<collection>
    'B': ['r', 'l', 't', 'c'],
    # Consume tokens from a bucket.
    # C;c=<collection>;b=<bucket>;t=<tokens>
    'C': ['t', 'c', 'b'],
}


_RESPS = {
    # Success.
    '+': [],
    # Action failed without an error, e.g. bucket exhausted.
    '-': [],
    # Error; 'm' attribute contains error message.
    # !;m=<msg>
    '!': ['m'],
}


class Handler(asynchat.async_chat):  # pylint: disable-msg=R0904
    """
    Handle charity domain queries.
    """

    def __init__(self, sock, db_path):
        asynchat.async_chat.__init__(self, sock)
        self.ibuffer = []
        self.set_terminator(CRLF)

    def collect_incoming_data(self, data):
        self.ibuffer.append(data)

    def found_terminator(self):
        request = ''.join(self.ibuffer)
        self.ibuffer = []
        self.push('Request was: [{0}]'.format(request))
        self.push(CRLF)


class UnixServer(asyncore.dispatcher):  # pylint: disable-msg=R0904
    """
    Simple listener that accepts incoming connections over a Unix stream
    socket and spawns per-connection handlers.
    """

    def __init__(self, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.bind(path)
        self.listen(128)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, _ = pair
            Handler(sock)
