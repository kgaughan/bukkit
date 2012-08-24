import SocketServer
import socket

from bukkit import bucket


_REQS = {
    'B': ('r', 'l', 't', 'c'),
    'C': ('t', 'c', 'b')}


_RESPS = {
    '+': (),
    '-': (),
    '!': ('m',)}


class ProtocolError(Exception):
    """
    """

    __slots__ = ()


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


class RequestHandler(SocketServer.StreamRequestHandler):
    """
    Simple request handler for a simple stream-based protocol for managing
    a set of token bucket collections. Responses are terminated by
    double-linefeeds. In the descriptions, semicolons are used to represent
    linefeeds for compactness. Field order within requests can vary, but the
    command line must always come first. Responses 

    Request format:
      B;r=<rate>;l=<limit>;t=<timeout>;c=<collection>
        - Create a bucket collection with the given settings. Always responds
          with '+'. Note that if a collection already exists with the given
          name, it will be destroyed.
      C;c=<collection>;b=<bucket>;t=<tokens>
        - Attempt to consume the given tokens from the named bucket in the
          named collection. Response is '+'if successful, '-' if not.

      If the response code starts with '!', an error message follows in the
      'm' attribute.
    """

    collections = {}

    def _send(self, stanza_type, attrs=None):
        self.wfile.write(_build_stanza(stanza_type, attrs))

    def error(self, msg):
        self._send('!', {'m': msg})

    def success(self):
        self._send('+')

    def failure(self):
        self._send('-')

    def handle(self):
        try:
            cmd, attrs = _read_stanza(self.rfile, _REQS)
            if cmd == 'B':
                self.handle_create(
                    rate=attrs['r'],
                    limit=attrs['l'],
                    timeout=attrs['t'],
                    collection=attrs['c'])
            elif cmd == 'C':
                self.handle_consume(
                    collection=attrs['c'],
                    name=attrs['b'],
                    tokens=attrs['t'])
            else:
                self.error('WAT')
        except ProtocolError, exc:
            self.error(exc.message)

    def handle_create(self, rate, limit, timeout, collection):
        self.collections[collection] = bucket.Collection(
            rate=rate, limit=limit, timeout=timeout)
        self.success()

    def handle_consume(self, collection, name, tokens):
        if collection not in self.collections:
            self.error("'%s' is not a known bucket collection" % collection)
        elif self.collections[collection].consume(name, tokens):
            self.success()
        else:
            self.failure()


class Client(object):

    __all__ = ('sock',)

    def __init__(self, path):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(path)

    def _send(self, cmd, attrs):
        self.sock.sendall(_build_stanza(cmd, attrs))

    def create(self, rate, limit, timeout, collection):
        self._send('B', {'r': rate, 'l': limit, 't': timeout, 'c': collection})

    def consume(self, collection, name, tokens):
        self._send('C', {'c': collection, 'b': name, 't': tokens})


def run_server():
    server = SocketServer.UnixStreamServer(
        '/tmp/bukkit.sock', RequestHandler)
    server.serve_forever()
