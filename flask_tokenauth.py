"""
flask_tokenauth
==================

This module provides token-based authentication for Flask routes.

:copyright: (C) 2016 by Alex Forbes.
:license:   BSD, see LICENSE for more details.
"""
from __future__ import print_function, unicode_literals, absolute_import, \
    division
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from functools import wraps
from flask import request, make_response
from six import string_types

__author__ = 'alforbes'

"""
Flask module for token authentication, using itsdangerous for actual crypto

This module borrows heavily from Flask-HTTPAuth, and Miguel Grinberg's blog
at http://blog.miguelgrinberg.com/

Many thanks to Miguel for his great contributions!
"""


class TokenAuthError(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class TokenManager(object):
    """ Create and verify Tokens
    """
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate(self, name, expiration=3600):
        s = Serializer(self.secret_key, expires_in=expiration)
        return s.dumps({'id': name})

    def verify(self, token):
        if not token:
            return None
        s = Serializer(self.secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        name = data['id']
        return name

    # Not finished
    def store(self, f):
        """ Optionally specify a function to store a token

        :param f:
        """
        # self.store_token_callback = f
        # return f
        raise NotImplementedError

    def retrieve(self, f):
        """ Optionally specify a function to retrieve a token

        :param f: Function to use
        """
        # self.retrieve_token_callback = f
        # return f
        raise NotImplementedError


class TokenAuth(object):
    """ Authenticate a token

    Takes X-Auth-Token header and extracts a user name value from it using a
    given TokenManager.
    """
    def __init__(self, secret_key, realm=None):
        def default_error_handler():
            return "Access Denied"

        self.token_manager = TokenManager(secret_key=secret_key)
        self.realm = realm or "Authentication Token Required"

        self.verify_token(None)
        self.error_handler(default_error_handler)

    def error_handler(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            res = f(*args, **kwargs)
            if isinstance(res, string_types):
                res = make_response(res)
                res.status_code = 401
            if 'WWW-Authenticate' not in res.headers.keys():
                res.headers['WWW-Authenticate'] = 'Token realm="{}"'.format(self.realm)
            return res
        self.auth_error_callback = decorated
        return decorated

    def token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('X-Auth-Token')
            if not token:
                return self.auth_error_callback()
            if not self.authenticate(token):
                return self.auth_error_callback()
            return f(*args, **kwargs)
        return decorated

    def authenticate(self, token):
        """ Authenticate a token

        :param token:
        """
        if self.verify_token_callback:
            # Specified verify function overrides below
            return self.verify_token_callback(token)

        if not token:
            return False

        name = self.token_manager.verify(token)
        if not name:
            return False

        return True

    def verify_token(self, f):
        """ Optionally specify a function to perform the token verification

        For example, if it is present in a database.
        By default we just check we can decode it with our secret.

        :param f:
        """
        self.verify_token_callback = f
        return f

