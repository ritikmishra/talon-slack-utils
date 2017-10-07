"""Run the server for the slack stuff."""
import os

import tornado.httpclient
import tornado.ioloop
import tornado.testing
import tornado.web

from .exchange_bit import BTCExchangeRateHandler
from .params import params_from_request
from all.talker.talker import Talker

try:
    PORT = os.environ['PORT']
except KeyError:
    PORT = 8888



talker = Talker()




class ThinkHandler(tornado.web.RequestHandler):
    """Handle requests for creating crap English sentences."""

    def prepare(self):
        """Prepare for handling the request."""
        self.params = params_from_request(self.request)
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


def main():
    app = make_app()
    app.listen(PORT)
    print("Listening on port " + str(PORT))
    tornado.ioloop.IOLoop.current().start()
