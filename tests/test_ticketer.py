#!/usr/bin/env
import os
import unittest
import ticketer

from ticketer.main import get_connection
from ticketer.main import get_cursor
from ticketer.main import init_db
from werkzeug import generate_password_hash, check_password_hash


class TicketerTestCase(unittest.TestCase):

    def setUp(self):
        ticketer.app.config['TESTING'] = True
        self.app = ticketer.app.test_client()
        with ticketer.app.app_context():
            self.db_connection = get_connection()
            self.db_cursor = get_cursor()
            init_db()

    def tearDown(self):
        self.db_cursor.close()
        #self.db_connection.close()

    def test_hi(self):
        resp = self.app.get("/hi")
        assert resp.status == '200 OK'
        assert resp.data == 'hi'

    def test_index(self):
        resp = self.app.get("/")
        assert resp.status == '200 OK'
        assert 'Ticketing App' in resp.data

    def signup(self, name, email, password):
        return self.app.post('/signUp', 
                             data=dict(inputName=name, inputEmail=email, inputPassword=password),
                             follow_redirects=True)

    def test_signup(self):
        resp = self.signup('name', 'name@something.com', 'Pa55W04d')
        assert resp.status == '200 OK'

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
