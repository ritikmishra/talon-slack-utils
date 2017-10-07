"""Test for Travis CI, as we cannot break poor little Titanium when working on it."""
import tornado.testing
from all.server import server_main


class ServerTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return server_main.make_app()

    def test_exchange(self):
        """Test that we can find the exchange rate between Dollars and Euros"""
        response = self.fetch("/exchange?text=USD EUR")
        # Test contents of response
        print(response.body)
        self.assertIn(b"USD", response.body)
        self.assertIn(b"EUR", response.body)
        self.assertEqual(response.code, 200)

    def test_triple_exchange(self):
        """Test that we can find the exchange rate between USD and EUR as well as USD and CAD"""
        response = self.fetch("/exchange?text=USD EUR CAD")
        # Test contents of response
        print(response.body)
        self.assertIn(b"USD", response.body)
        self.assertIn(b"EUR", response.body)
        self.assertIn(b"CAD", response.body)
        self.assertEqual(response.code, 200)

    def test_btc_triple_exchange(self):
        """Test that we can find the exchange rate between BTC and multiple other currencies"""
        response = self.fetch("/exchange?text=BTC EUR CAD")
        # Test contents of response
        print(response.body)
        self.assertIn(b"BTC", response.body)
        self.assertIn(b"EUR", response.body)
        self.assertIn(b"CAD", response.body)
        self.assertEqual(response.code, 200)

    def test_triple_exchange(self):
        """Test that we can find the exchange rate between BTC and one other currency"""
        response = self.fetch("/exchange?text=BTC EUR")
        # Test contents of response
        print(response.body)
        self.assertIn(b"BTC", response.body)
        self.assertIn(b"EUR", response.body)
        self.assertEqual(response.code, 200)

    def test_thinker(self):
        response = self.fetch("/think?text=USD")
        # Test contents of response
        self.assertEqual(response.code, 200)


