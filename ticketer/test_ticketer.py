#!/usr/bin/env
import unittest
import ticketer
import requests

class TestIt(unittest.TestCase):

    """
    This test set exercises the flask app for ticketer
    """ 

    URL = "http://localhost:" + str(ticketer.port) + "/"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_isrunning(self):
        rv = requests.get(TestIt.URL)
        assert (rv.status_code >= 200 and rv.status_code < 300), "Bad return code = " + str(rv.status_code)
