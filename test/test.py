import unittest
import requests

class TestPostRequests(unittest.TestCase):
    def test_loc(self):
        r = requests.post(url = "http://127.0.0.1:5000/safety/loc", json = {"location": "1,1"})
        print r.json()
        self.assertEqual(r.status_code, 200)

    def test_route(self):
        r = requests.post(url = "http://127.0.0.1:5000/safety/route", json = {"locations": ["34,12", "33,33"]})
        print r.json()
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()