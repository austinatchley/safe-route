import unittest
import requests

class TestPostRequests(unittest.TestCase):
    def test_loc(self):
        r = requests.post(url = "http://127.0.0.1:5000/safety/loc", json = {"location": "test"})
        self.assertEqual(r.status_code, 200)

    def test_route(self):
        r = requests.post(url = "http://127.0.0.1:5000/safety/route", json = {"locations": ["test1", "test2"]})
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()