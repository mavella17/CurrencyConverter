import unittest
import requests
from capi_main import updateDB, printDB
from capi_main import getList, base


class TestFileName(unittest.TestCase):
	#These first 3 test cases only verify they run without errors
	#Not much other testing can be done here
    def testUpdate(self):
	    assertEquals(updateDB(), True)
    def testPrint(self):
        assertEquals(printDB(), True)
    def testList(self):
	    assertEquals(getList(), True)
if __name__ == '__main__':
    unittest.main()
