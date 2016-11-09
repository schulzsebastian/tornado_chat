from app import app
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop


clients = []


class WebSocket(WebSocketHandler):
    def open(self, room):
        self.__room = room
        clients.append(self)
        print("User connected")

    def on_message(self, message):
        print('User sent: {}'.format(message))
        for client in clients:
            if client.__room == self.__room:
                client.write_message('You sent: {}'.format(message))

    def on_close(self):
        print("User disconnected")

if __name__ == "__main__":
    container = WSGIContainer(app)
    server = Application([
        (r'/websocket/(.*)', WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ], debug=True)
    server.listen(5000)
    IOLoop.instance().start()
