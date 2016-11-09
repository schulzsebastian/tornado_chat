from app import app
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop, PeriodicCallback
import random
import string


class WebSocket(WebSocketHandler):
    clients = []

    def open(self, room):
        self.__room = room
        self.clients.append(self)
        print("User connected")

    def on_message(self, message):
        print('User sent: {}'.format(message))
        for client in self.clients:
            if client.__room == self.__room:
                client.write_message('You sent: {}'.format(message))

    def on_close(self):
        self.clients.remove(self)
        print("User disconnected")


def test_messages():
    msg = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
    for client in WebSocket.clients:
        client.write_message('Server message: {}'.format(msg))

if __name__ == "__main__":
    container = WSGIContainer(app)
    server = Application([
        (r'/websocket/(.*)', WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ], debug=True)
    server.listen(5000)
    main_loop = IOLoop.instance()
    event_test_messages = PeriodicCallback(
        test_messages,
        500,
        io_loop=main_loop)
    event_test_messages.start()
    main_loop.start()
