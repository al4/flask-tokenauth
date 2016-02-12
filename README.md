Flask-TokenAuth
===============

Provides Token authentication for Flask routes.

Installation
------------
The easiest way to install this is through pip.
```
pip install Flask-TokenAuth
```

Basic authentication example
----------------------------

```python
from flask import Flask
from flask_TokenAuth import TokenAuth, TokenManager

app = Flask(__name__)
token_auth = TokenAuth()
token_manager = TokenManager(secret_key='really big secret')

@token_auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.token_required
def index():
    return "Hello, %s!" % auth.username()

if __name__ == '__main__':
    app.run()
```

Resources
---------

- [Documentation](http://pythonhosted.org/Flask-HTTPAuth)
- [pypi](https://pypi.python.org/pypi/Flask-TokenAuth)

