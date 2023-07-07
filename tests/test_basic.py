import unittest, sys

sys.path.append('../CurrencyConverter') # imports python file from parent directory
from webPage import app #imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_convert_page(self):
        response = self.app.get('/convert', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)    

if __name__ == "__main__":
    unittest.main()