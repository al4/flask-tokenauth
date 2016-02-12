from flask import Flask, g
from flask_tokenauth import TokenAuth, TokenManager

app = Flask(__name__)
secret_key = 'really big secret'
token_auth = TokenAuth(secret_key=secret_key)
token_manager = TokenManager(secret_key=secret_key)

users = {
    'bob': None
}


@app.route('/')
@token_auth.token_required
def index():
    return "Hello, {}!".format(g.current_user)


@app.route('/token/<username>')
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
