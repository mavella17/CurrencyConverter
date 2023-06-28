import unittest
import requests
from capi_main import updateDB, printDB
from capi_main import getList, base_exchange
from capi_main import checkValidCurrency
from unittest.mock import patch


class TestFileName(unittest.TestCase):

    # These first 3 test cases only verify they run without errors
    # Not much other testing can be done here
    def testUpdate(self):
        self.assertEqual(updateDB(), True)

    def testPrint(self):
        self.assertEqual(printDB(), True)

    def testList(self):
        self.assertEqual(getList(), True)

    def testValidCurr(self):
        self.assertEqual(checkValidCurrency('usd'), True)
        self.assertEqual(checkValidCurrency('usd213132'), False)
        self.assertEqual(checkValidCurrency('USD'), True)
        self.assertEqual(checkValidCurrency('uSd'), True)

    inputs = ['b', 'eur', 'jpy', '1']

    @patch('builtins.input', side_effect=inputs)
    def testBaseExchange(self, mock_input):
        url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/'
        urlbase = url + 'currency-api@1/latest/currencies/'
        r = requests.get(urlbase + 'eur/jpy.json').json()['jpy']
        self.assertEqual(base_exchange(), r)
        self.assertEqual(base_exchange('eur', 'jpy', 1), r)
        r = requests.get(urlbase + 'usd/gbp.json').json()['gbp']
        self.assertEqual(base_exchange('usd', 'gbp', 45), 45 * r)
        r = requests.get(urlbase + 'usd/gbp.json').json()['gbp']
        self.assertEqual(base_exchange('usd', 'gbp', -45), -45 * r)

    inputs = ['b', 'euooooo', 'eur', 'gibberish', 'doesntwork', 'jpy', '1']

    @patch('builtins.input', side_effect=inputs)
    def testInvalidBase(self, mock_input):
        url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/'
        urlbase = url + 'currency-api@1/latest/currencies/'
        r = requests.get(urlbase + 'eur/jpy.json').json()['jpy']
        self.assertEqual(base_exchange(), r)

    inputs = ['b', 'usd', 'all', 'yur', 'yes', 'y', 'Y', 'y', 'yessum', 'y']
    inputs += ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y']
    inputs += ['y', 'y', 'y', 'dsada', 'y']

    @patch('builtins.input', side_effect=inputs)
    def testBasetoAll(self, mock_input):
        self.assertEqual(base_exchange(), True)

    inputs += ['b', 'usd', 'all', 'yes', 'no']

    @patch('builtins.input', side_effect=inputs)
    def testInvalidBase2(self, mock_input):
        self.assertEqual(base_exchange(), True)


if __name__ == '__main__':
    unittest.main()
