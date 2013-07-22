import SocketServer
import socket

from bukkit import bucket, client


_REQS = {
    'B': ('r', 'l', 't', 'c'),
    'C': ('t', 'c', 'b'),
}


_RESPS = {
    '+': (),
    '-': (),
    '!': ('m',),
}


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
        self.wfile.write(client._build_stanza(stanza_type, attrs))

    def error(self, msg):
        self._send('!', {'m': msg})

    def success(self):
        self._send('+')

    def failure(self):
        self._send('-')

    def handle(self):
        try:
            cmd, attrs = client._read_stanza(self.rfile, _REQS)
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
        except client.ProtocolError as exc:
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


def run_server():
    server = SocketServer.UnixStreamServer(
        '/tmp/bukkit.sock', RequestHandler)
    server.serve_forever()
