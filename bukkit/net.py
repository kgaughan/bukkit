import SocketServer
import socket


class BucketRequestHandler(SocketServer.BaseRequestHandler):
    """
    Simple request handler for a simple stream-based protocol for managing
    a set of token bucket collections. Responses are terminated by linefeeds.

    Datagram format:
      B;<rate>;<limit>;<timeout>;<collection>
        - Create a bucket collection with the given settings. No response.
      C;<tokens>;<collection>;<bucket>
        - Attempt to consume the given tokens from the named bucket in the
          named collection. Response is '+'if successful, '-' if not.
      Q;<collection>;<bucket>
        - Query the token count for the given bucket in the given collection.
          Response will be '<available>;<limit>'.
    """

    def handle(self):
        pass


def client():
    pass


def run_server():
    server = SocketServer.UnixStreamServer(
        '/tmp/bukkit.sock', BucketRequestHandler)
    server.serve_forever()
