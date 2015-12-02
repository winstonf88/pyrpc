import tornado.websocket
import tornado.gen

from pyrpc.jsonrpc import JsonRenderer
from pyrpc.request import parse_procedure


class JsonRPCWebsocketHandler(tornado.websocket.WebSocketHandler):
    """Tornado JSON RPC Websocket Handler."""
    renderer = JsonRenderer()

    @tornado.gen.coroutine
    def on_message(self, message):
        response = parse_procedure(message, self.renderer, socket=self)
        self.write_message(response)
