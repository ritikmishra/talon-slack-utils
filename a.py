import tornado.gen
import tornado
@gen.coroutine
def main(base, currencies, currency):
    """Get the exchange rates for the specified currencies."""

    http_client = tornado.httpclient.AsyncHTTPClient()
    print("Base", self.base)
    print("Symbols", self.currencies)
    print("URL", "https://api.fixer.io/latest?base=" + self.base + "&symbols=" + ",".join(self.currencies))
    response = yield http_client.fetch(
        "https://api.fixer.io/latest?base=" + self.base + "&symbols=" + ",".join(self.currencies))

    # how many of each other currency
    data = tornado.escape.json_decode(response.body)["rates"][self.currency]
    yield data

if __name__ == '__main__':
    print(main())