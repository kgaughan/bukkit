"""
"""

import socket


__all__ = (
    'ProtocolError',
    'Client',
)


class ProtocolError(Exception):
    """
    """


def _read_stanza(rfile, allowed):
    stanza_type = rfile.readline().rstrip("\n")
    if stanza_type not in allowed:
        raise ProtocolError("'%s' is not recognised" % stanza_type)

    attrs = allowed[stanza_type]
    collected = {}
    for line in rfile:
        line = line.rstrip("\n")
        if len(line) == 0:
            break
        if len(collected) > len(attrs):
            raise ProtocolError("Too many attributes; max is %d" % len(attrs))
        parts = line.split(1, '=')
        if len(parts) != 2:
            raise ProtocolError("'%s' is not an attribute line" % line)
        key, value = parts
        if key in collected:
            raise ProtocolError("'%s' provided multiple times" % key)
        if key not in attrs:
            raise ProtocolError("'%s' is not a valid attribute" % key)
        collected[key] = value

    return stanza_type, attrs


def _build_stanza(stanza_type, attrs=None):
    if attrs is None:
        attrs = {}
    return "\n".join(
        [stanza_type] +
        [key + '=' + value for key, value in attrs.iteritems()]) + "\n\n"


class Client(object):

    __all__ = (
        'sock',
    )

    def __init__(self, path):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(path)

    def _send(self, cmd, attrs):
        self.sock.sendall(_build_stanza(cmd, attrs))

    def create(self, rate, limit, timeout, collection):
        self._send('B', {'r': rate, 'l': limit, 't': timeout, 'c': collection})

    def consume(self, collection, name, tokens):
        self._send('C', {'c': collection, 'b': name, 't': tokens})
