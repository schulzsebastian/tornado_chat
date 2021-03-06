from app import app
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop, PeriodicCallback
from datetime import datetime
import json
import random
import string


class WebSocket(WebSocketHandler):
    clients = []

    def open(self, room):
        self.__room = room
        self.clients.append(self)
        print("User connected")

    def on_message(self, payload):
        msg = json.loads(payload)
        if msg['type'] == 'message':
            for client in self.clients:
                if client.__room == self.__room:
                    client.write_message(payload)

    def on_close(self):
        self.clients.remove(self)
        print("User disconnected")

if __name__ == "__main__":
    container = WSGIContainer(app)
    server = Application([
        (r'/websocket/(.*)', WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ], debug=True)
    server.listen(5000)
    main_loop = IOLoop.instance()
    main_loop.start()
