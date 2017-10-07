import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.testing
from tornado import gen
from talker import Talker
import os
from server.params import params_from_request


class BTCExchangeRateHandler(tornado.web.RequestHandler):
    """Handle requests to find out the exchange rate."""

    def prepare(self):
        """Prepare for handling the request."""
        self.base = "USD"
        self.btc = False
        self.params = params_from_request(self.request)
        self.resjson = {"response_type": "in_channel"}
        if len(self.params['text']) == 0:
            self.currencies = ["EUR"]
        else:
            self.currencies = self.params['text'].upper().split(" ")
            self.base = self.currencies[0]
            if self.base == "BTC":
                self.base = "USD"
                self.btc = True

        self.add_header("Content-type", "application/json")

    def expand_currency_abbv(self, abbv):
        """Expand currency abbreviations."""
        return self.currencies_expanded[self.currencies_abbreviated.index(abbv)]

    @staticmethod
    def interlace(list_a, list_b):
        """Interlace 2 lists."""
        result = []
        for x in range(len(list_a)):
            pair = []
            pair.append(list_a[x])
            pair.append("(" + list_b[x] + ")")
            result.append(" ".join(pair))
        return result

    @gen.coroutine
    def get_all(self):
        result = []
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = yield http_client.fetch("https://api.fixer.io/latest?base=" + self.base + "&symbols=" + ",".join(self.currencies))

        # how many of each other currency
        data = tornado.escape.json_decode(response.body)["rates"][self.currency]
        yield data

    @gen.coroutine
    def get_btc(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = yield http_client.fetch("http://blockchain.info/ticker")
        data = tornado.escape.json_decode(response.body)["USD"]["last"]
        yield float(data)


    @gen.coroutine
    def convert_btc(self):
        currency_per_usd = yield self.get_all()

        # a number
        usd_per_btc = yield self.get_btc()

        currency_per_btc = {}
        for currency in currency_per_usd:
            currency_per_usd[currency] = usd_per_btc * currency_per_usd[currency]

    def format_nums(self, currency_per_base):
        result = []
        for currency, rate in currency_per_base.items():
            result.append("1 " + self.base + " is worth " + rate + " " + currency)
        return "\n".join(result)


    @gen.coroutine
    def post(self):
        """Handle POST requests."""
        if self.btc:
            data = yield self.convert_btc()

        self.resjson['text'] = yield self.get_btc()
        self.write(self.resjson)

    @gen.coroutine
    def get(self):
        """Handle GET requests when testing."""
        yield self.post()  # you need to use the 'yield' keyword since self.post() is a coroutine
