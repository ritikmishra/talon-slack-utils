"""Run the server for the slack stuff."""
import tornado.ioloop
import tornado.web
import tornado.httpclient
from main import Talker
import os
# url = "https"
try:
    PORT = os.environ['PORT']
except KeyError:
    PORT = 8888


def paramsfromrequest(request):
    """Change the format of the HTTP request parameters so that they may be more easily used."""
    params_dict = {}
    for key, value in request.arguments.items():
        if len(value) == 1:
            params_dict[key] = value[0].decode('UTF-8')
        else:
            params_dict[key] = []
            for part in value:
                params_dict[key].append(part.decode('UTF-8'))
    return params_dict


talker = Talker()


class BTCExchangeRateHandler(tornado.web.RequestHandler):
    """Handle requests to find out the bitcoin exchange rate."""

    def prepare(self):
        """Prepare for handling the request."""
        self.currencies_expanded = ["New Zealand Dollar", "Swedish Krona", "Icelandic Krona",
                                    "Japanese Yen", "Singapore Dollar", "Euro", "British Pound",
                                    "New Taiwan Dollar", "Chinese Yuan", "Canadian Dollar", "Polish Zloty",
                                    "Danish Krone", "South Korean Won", "Australian Dollar",
                                    "Chilean Peso", "Indian Rupee", "Swiss Franc", "Thai Bhat",
                                    "Brazilian Real", "US Dollar", "Russian Ruble", "Hong Kong Dollar"]

        self.currencies_abbreviated = ["NZD", "SEK", "ISK", "JPY", "SGD", "EUR", "GBP", "TWD", "CNY", "CAD", "PLN",
                                       "DKK", "KRW", "AUD", "CLP", "INR", "CHF", "THB", "BRL", "USD", "RUB", "HKD"]

        self.params = paramsfromrequest(self.request)
        self.resjson = {"response_type": "in_channel"}
        if len(self.params['text']) == 0:
            self.currency = "USD"
        else:
            self.currency = self.params['text']
        self.currency = self.currency.upper()
        self.add_header("Content-type", "application/json")

    def expandCurrency(self, abbv):
        """Expand currency abbreviations."""
        return self.currencies_expanded[self.currencies_abbreviated.index(abbv)]

    def interlace(self, list_a, list_b):
        """Interlace 2 lists."""
        result = []
        for x in range(len(list_a)):
            pair = []
            pair.append(list_a[x])
            pair.append("(" + list_b[x] + ")")
            result.append(" ".join(pair))
        return result

    def post(self):
        """Handle POST requests."""
        try:
            self.http_client = tornado.httpclient.HTTPClient()
            self.response = self.http_client.fetch("http://blockchain.info/ticker")
            self.all_data = tornado.escape.json_decode(self.response.body)

        except tornado.httpclient.HTTPError as number:
            self.resjson['text'] = "The Exchange Rate API we use gave us the following error code: " + str(number)

        try:
            self.data = self.all_data[self.currency]
            self.resjson['text'] = "1 BitCoin is equal to " + str(self.data["last"]) + " " + self.expandCurrency(self.currency)

        except (KeyError, ValueError, IndexError):
            self.resjson['text'] = "I cannot find data on your currency. I can find data on the following currencies: " + ", ".join(self.interlace(list(self.currencies_abbreviated), self.currencies_expanded))

        except Exception as e:
            self.resjson['text'] = str(e)
            raise Exception

        finally:
            self.write(self.resjson)

    def get(self):
        """Handle GET requests."""
        self.post()


class ThinkHandler(tornado.web.RequestHandler):
    """Handle requests for creating crap English sentences."""

    def prepare(self):
        """Prepare for handling the request."""
        self.params = paramsfromrequest(self.request)
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
