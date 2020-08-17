import sys
import os
import unittest
import json
import xmlrunner
import time

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../')))
    
import app

class TestAppUrl(unittest.TestCase):
    """
    Test Case for Testing Authenticate API
    """
    def setUp(self):
        print(f"Executing: {self._testMethodName} ")
        self.start_time = time.time()
        self.app = app.app.test_client()
        pass

    def tearDown(self):
        print(f"TestCase: {self._testMethodName} executed in: {time.time()-self.start_time} Secs")
        pass

    def test_about(self):
        fake_req = self.app.get('/about')
        print(fake_req.data)
        self.assertIsNotNone(fake_req)

    def test_fetch(self):
        fake_req = self.app.get('/fetch/all')
        print(json.loads(fake_req.data))
        self.assertIsNotNone(fake_req)
    
    def test_by_month(self):
        fake_req = self.app.get('/fetch/month/Jan')
        print(json.loads(fake_req.data))
        self.assertIsNotNone(fake_req)

    def add_by_month(self):
        data = [
            {
                "amount": "299", "cardType": "Black",
                "category": "WALLET", "desc": "Test",
                "tran_date": "2020-03-12"},
             {
                "amount": "500", "cardType": "Silver",
                "category": "WALLET", "desc": "TestSilver",
                "tran_date": "2020-12-12"
            }
        ]
        body = json.dumps(data)
        fake_req = self.app.post('/upload', data=body)
        print(json.loads(fake_req.data))
        self.assertIsNotNone(fake_req)

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
