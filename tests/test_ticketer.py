#!/usr/bin/env
import os
import unittest
import ticketer

from ticketer.main import get_connection
from ticketer.main import get_cursor
from ticketer.main import init_db
from werkzeug import generate_password_hash, check_password_hash


class TicketerTestCase(unittest.TestCase):

    username = "name"
    user_email = "name@something.com"
    unknown_email = "other@something.com"
    password = "Pa55w04d"
    bad_password = "not-a-good-password"

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
        resp = self.signup(self.username, 
                           self.user_email,
                           self.password)
        assert resp.status == '200 OK'

    def login(self, user_email, password):
        return self.app.post('/validateLogin', data=dict(
            inputEmail=user_email,
            inputPassword=password
        ), follow_redirects=True)

    def test_good_login(self):
        resp = self.login(self.user_email, self.password)
        assert resp.status == '200 OK'

    def test_bad_login(self):
        resp = self.login(self.user_email, self.bad_password)
        assert resp.status == '200 OK'
        assert "Wrong Email address or Password" in resp.data

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_logout(self):
        resp = self.logout()
        assert resp.status == '200 OK'

if __name__ == '__main__':
    unittest.main()
