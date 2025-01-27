import os

import flask        # Libraries for WEB page
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

import folium       # Libraries for map
from folium import ClickForMarker

from sqlalchemy import create_engine, select    # Libraries for DataBase
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from models.user_model import User         # Imports from other files
from models.announ_model import Annoucement as ann


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
engine = create_engine("sqlite:///DB/PetHunt.db", echo=True)    # page initial
session = Session(engine)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")         #TODO: Main Page
@app.route("/index")
def home():
    return render_template("index.html", current_user=current_user)


@app.route("/register", methods=["POST", "GET"])        # register page
def register():
    if flask.request.method == "POST":
        if session.query(User).filter(User.login == request.form['login']).first():
            return render_template('register.html', title='Регистрация',
                                   message="Такой пользователь уже есть")
        log = request.form['login']
        pas = request.form['password']
        fio = request.form['fio']
        phone = request.form['phone']
        ds = request.form['area']
        if log is not None and pas is not None and fio is not None and phone is not None and ds is not None:
            usr = User(
                full_name = fio,
                login = log,
                password = generate_password_hash(pas),
                phone = phone,
                district = ds
            )
            session.add(usr)
            session.commit()
            return redirect('/index')
    return render_template("register.html")


@app.route("/proba", methods=["POST", "GET"])
def proba():
    return render_template("SAiti.html")


@app.route("/login", methods=["POST", "GET"])           # login page
def login():
    if flask.request.method == "POST":
        log = request.form['log']
        pas = request.form['pas']
        user = session.query(User).filter(User.login == log).first()
        if user and check_password_hash(str(user.password), pas):
            login_user(user)
            print(current_user.is_authenticated)
            return redirect('/index')
        return render_template('login.html')
    else:
        return render_template("login.html")


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/add", methods=["POST", "GET"])         # add page
def add():
    return render_template("add.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
