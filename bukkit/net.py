import SocketServer
import socket

from bukkit import bucket


class BucketRequestHandler(SocketServer.BaseRequestHandler):
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

      If the response code starts with '!', an error message follows on the
      next line.
    """

    attrs = {
        'B': ('r', 'l', 't', 'c'),
        'C': ('t', 'c', 'b')}

    collections = {}

    def error(self, msg):
        self.wfile.write("!\n%s\n\n" % msg)

    def success(self):
        self.wfile.write("+\n\n")

    def failure(self):
        self.wfile.write("-\n\n")

    def handle(self):
        cmd = self.rfile.readline().rstrip("\n")
        if cmd not in self.attrs:
            self.error("'%s' is not a valid command" % cmd)
            return
        attrs = self.attrs[cmd]
        collected = {}
        for line in lines:
            line = line.rstrip("\n")
            if len(line) == 0:
                break
            if len(collected) > len(attrs):
                self.error("Too many attributes; max is %d" % len(attrs))
                return
            parts = line.split(1, '=')
            if len(parts) != 2:
                self.error("'%s' is not an attribute line" % line)
                return
            key, value = parts
            if key in collected:
                self.error("'%s' provided multiple times" % key)
                return
            if key not in attrs:
                self.error("'%s' is not a valid attribute" % key)
                return
            collected[key] = value
        if cmd == 'B':
            self.handle_create(
                rate=attrs['r'],
                limit=attrs['l'],
                timeout=attrs['t'],
                collection=attrs['c'])
        elif cmd == 'C':
            self.handle_consume(
                collection=attrs['c'],
                bucket=attrs['b'],
                tokens=attrs['t'])

    def handle_create(self, rate, limit, timeout, collection):
        self.collections[collection] = bucket.Collection(
            rate=rate, limit=limit, timeout=timeout)
        self.success()

    def handle_consume(self, collection, bucket, tokens):
        if collection not in collections:
            self.error("'%s' is not a known bucket collection" % collection)
            return
        if self.collections[collection].consume(bucket, tokens):
            self.success()
        else:
            self.failure()


def client():
    pass


def run_server():
    server = SocketServer.UnixStreamServer(
        '/tmp/bukkit.sock', BucketRequestHandler)
    server.serve_forever()
