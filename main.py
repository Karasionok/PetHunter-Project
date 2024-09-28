from flask import Flask, render_template, redirect, request, session, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
