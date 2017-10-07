"""Run the server for the slack stuff."""
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.testing
from tornado import gen
from talker import Talker
import os
from exchange_bit import BTCExchangeRateHandler

try:
    PORT = os.environ['PORT']
except KeyError:
    PORT = 8888



talker = Talker()




class ThinkHandler(tornado.web.RequestHandler):
    """Handle requests for creating crap English sentences."""

    def prepare(self):
        """Prepare for handling the request."""
        self.params = params(self.request)
        self.resjson = {"response_type": "in_channel"}
        self.words = []
        try:
            for word in self.params['text']:
                if (not word[0] == "<") and (not word[-1] == ">"):
                    self.words.append(word)
            self.words = " ".join(self.words)
        except KeyError:
            self.words = " "
        self.add_header("Content-type", "application/json")

    def post(self):
        """Respond to POST requests."""
        self.resjson['text'] = talker.speak(self.words)
        self.write(self.resjson)

    def get(self):
        """Respond to GET requests."""
        self.post()


def make_app():
    """Assign handlers."""
    return tornado.web.Application([
        (r"/think", ThinkHandler),
        (r"/exchange", BTCExchangeRateHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    print("Listening on port " + str(PORT))
    tornado.ioloop.IOLoop.current().start()
