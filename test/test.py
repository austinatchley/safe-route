import unittest
import requests

class TestPostRequests(unittest.TestCase):
    def test_point(self):
        r = requests.post(url = "http://127.0.0.1:5000/safety/point", params = {})
        print r.json()
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()