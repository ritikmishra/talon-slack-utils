"""Test for Travis CI, as we cannot break poor little Titanium when working on it."""
import tornado.httpclient
import tornado.ioloop
import server
import os
import thread

try:
    PORT = os.environ['PORT']
except KeyError:
    PORT = 8888

if __name__ == "__main__":
    app = server.make_app()
    app.listen(PORT)




