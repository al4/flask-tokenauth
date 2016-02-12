Flask-TokenAuth
===============

Flask module for token authentication, using itsdangerous for the serialization and crypto.

This module borrows heavily from Flask-HTTPAuth, and Miguel Grinberg's blog at
http://blog.miguelgrinberg.com/

Many thanks to Miguel for his contributions!

Installation
------------
```
pip install Flask-TokenAuth
```

Basic authentication example
----------------------------

```python
from flask import Flask, g
from flask_tokenauth import TokenAuth, TokenManager

app = Flask(__name__)
secret_key = 'really big secret'
token_auth = TokenAuth(secret_key=secret_key)
token_manager = TokenManager(secret_key=secret_key)

users = ['bob']

@app.route('/')
@token_auth.token_required
def index():
    return "Hello, {}!".format(g.current_user)


@app.route('/token/<username>')
# @auth.login_required <-- use another module for this
def get_token(username=None):
    token = token_manager.generate(username)
    return token


@token_auth.verify_token
def verify_token(token):
    username = token_manager.verify(token)
    if username in users:
        g.current_user = username
        return True
    return None


if __name__ == '__main__':
    app.run()
```

Footnotes
---------
Obviously, you will want to authenticate users before allowing them to generate a token.
For this I suggest [Flask-HTTPAuth](http://pythonhosted.org/Flask-HTTPAuth) or a similar module.


Resources
---------

- [Documentation](http://pythonhosted.org/Flask-TokenAuth)
- [pypi](https://pypi.python.org/pypi/Flask-TokenAuth)

