import tornado.httpclient
import tornado.ioloop
import tornado.testing
import tornado.web
from tornado import gen

from .params import params_from_request


class ExchangeRateHandler(tornado.web.RequestHandler):
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
            self.currencies = self.currencies[1:]
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
        """Get the exchange rates for the specified currencies."""
        result = {}

        http_client = tornado.httpclient.AsyncHTTPClient()
        print("Base", self.base)
        print("Symbols", self.currencies)
        print("URL", "https://api.fixer.io/latest?base=" + self.base + "&symbols=" + ",".join(self.currencies))
        response = yield http_client.fetch(
            "http://api.fixer.io/latest?base=" + self.base + "&symbols=" + ",".join(self.currencies))

        # how many of each other currency
        body = tornado.escape.json_decode(response.body)
        print(body)
        for currency in self.currencies:
            result[currency] = body["rates"][currency]
        print("Result", result)
        raise gen.Return(result)

    @gen.coroutine
    def get_btc(self):
        """Get the exchange rate between USD and BTC. Please"""
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = yield http_client.fetch("http://blockchain.info/ticker")
        data = tornado.escape.json_decode(response.body)["USD"]["last"]
        raise gen.Return(float(data))

    @gen.coroutine
    def convert_btc(self):
        """Convert the exchange rate for an arbitrary currency to USD into one for BTC."""
        currency_per_usd = yield self.get_all()

        # a number
        usd_per_btc = yield self.get_btc()

        currency_per_btc = {}

        for currency in currency_per_usd:
            currency_per_btc[currency] = usd_per_btc * currency_per_usd[currency]

        raise gen.Return(currency_per_btc)

    def format_nums(self, currency_per_base):
        """
        Turn a dictionary of the format:

        {"USD": 123, "EUR": 456}

        into

        "1 <base currency> is worth 123 USD.\n1 ABC is worth 456 EUR."

        """
        result = []
        if self.btc:
            self.base = "BTC"
        for currency, rate in currency_per_base.items():
            result.append("1 " + self.base + " is worth " + str(rate) + " " + currency)
        return "\n".join(result)

    @gen.coroutine
    def post(self):
        """Handle POST requests."""
        try:

            if self.btc:
                data = yield self.convert_btc()
                print("BTC")
            else:
                data = yield self.get_all()
                print("Not BTC")
        except KeyError:
            self.resjson['text'] = "I'm sorry, the European Central Bank does not list exchange" \
                                   "rates for one or more of those currencies"
            self.resjson['response_type'] = "ephemeral"
        else:
            print(data)
            self.resjson['text'] = self.format_nums(data)
        self.write(self.resjson)

    @gen.coroutine
    def get(self):
        """Handle GET requests when testing."""
        yield self.post()  # you need to use the 'yield' keyword since self.post() is a coroutine
