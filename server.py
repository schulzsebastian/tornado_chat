from app import app
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop

class WebSocket(WebSocketHandler):
    def open(self):
        print("Socket opened.")

    def on_message(self, message):
        self.write_message("Received: " + message)
        print("Received message: " + message)

    def on_close(self):
        print("Socket closed.")

if __name__ == "__main__":
    container = WSGIContainer(app)
    server = Application([
        (r'/websocket/', WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ], debug=True)
    server.listen(5000)
    IOLoop.instance().start()