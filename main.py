from flask import Flask, render_template, redirect, request, session, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return 'Hello'


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    pass


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
