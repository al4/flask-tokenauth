from __future__ import print_function
from flask import Flask, jsonify, g
from flask_tokenauth import TokenAuth, TokenManager
from werkzeug.datastructures import Headers
from werkzeug.test import Client
import base64
import json
import unittest

__author__ = 'alforbes'


class TokenAuthTestCase(unittest.TestCase):
    """
    Base test class to setup the app
    """

    # A couple of test routes which require auth, and return 200 if it succeeds

    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['TRAP_HTTP_EXCEPTIONS'] = True

        secret_key = 'really big secret'
        token_manager = TokenManager(secret_key)

        token_auth = TokenAuth(secret_key)

        @app.route('/token')
        def get_token():
            user = 'test_user'
            token = token_manager.generate(user)
            return jsonify({'token': token})

        @app.route('/')
        def root():
            return jsonify({'message': 'OK'})

        @app.route('/token_required')
        @token_auth.token_required
        def token_required():
            response = jsonify({'message': 'OK'})
            response.status_code = 200
            return response

        self.app = app
        self.client = app.test_client()
        self.secret_key = secret_key
        self.token_manager = token_manager

        return self.app

    def get_token(self):
        response = self.client.get('/token')
        return json.loads(response.data)['token']

    def get_with_token_auth(self, path, token):
        """
        Do a request with token auth

        :param path:
        :param token:
        """
        h = Headers()
        h.add('X-Auth-Token', token)
        response = Client.open(self.client, path=path, headers=h)
        return response

    def post_with_token_auth(self, path, token, data):
        """
        Do a request with token auth

        :param path:
        :param token:
        :param data:
        """
        h = Headers()
        h.add('X-Auth-Token', token)
        h.add('Content-Type', 'application/json')
        response = Client.open(self.client, method='POST', data=data, path=path, headers=h)
        return response


class TestAuthToken(TokenAuthTestCase):
    def test_token(self):
        """
        Test that we can fetch a token
        """
        response = self.client.get('/token')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json.loads(response.data))


class TestBase(TokenAuthTestCase):
    """
    Base tests which make sure the setup is OK
    """
    def test_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class TestTokenAuth(TokenAuthTestCase):
    """
    Test token authentication
    """

    def test_unauthorised(self):
        """
        Test that we get 401 without a token
        """
        response = self.client.get('token_required')
        self.assertEqual(response.status_code, 401)

    def test_authorised(self):
        """
        Test that we get 200 with a token
        """
        token = self.get_token()
        response = self.get_with_token_auth('token_required', token)
        self.assertEqual(response.status_code, 200)

    def test_with_bad_token(self):
        """
        Test that we get 401 with a bad token
        """
        token = 'foo'
        response = self.get_with_token_auth('token_required', token)
        self.assertEqual(response.status_code, 401)


class TestCustomVerify(TokenAuthTestCase):
    def setUp(self):
        super(TestCustomVerify, self).setUp()

        custom_token_auth = TokenAuth(self.secret_key)

        @custom_token_auth.verify_token
        def verify_token(token):
            user = self.token_manager.verify(token)
            g.user = user
            return True

        @self.app.route('/get_user')
        @custom_token_auth.token_required
        def get_user():
            return jsonify({
                'user': g.user
            })

        self.custom_token_auth = custom_token_auth

    def test_token_name(self):
        """
        Test that we get the correct name back from the token
        """
        token = self.get_token()
        response = self.get_with_token_auth('/get_user', token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['user'], 'test_user')


def suite():
    return unittest.makeSuite(TokenAuthTestCase)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
