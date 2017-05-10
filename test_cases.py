"""Test for Travis CI, as we cannot break poor little Titanium when working on it."""
import tornado.testing
import server


class ServerTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return server.make_app()

    def test_exchange(self):
        response = self.fetch("/exchange?text=USD")
        # Test contents of response
        self.assertIn(b"BitCoin", response.body)
        self.assertEqual(response.code, 200)

    def test_thinker(self):
        response = self.fetch("/think?text=USD")
        # Test contents of response
        self.assertEqual(response.code, 200)


