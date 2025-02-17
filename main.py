import os

import flask        # Libraries for WEB page
from flask import Flask, render_template, request, redirect, url_for, flash

import folium       # Libraries for map
from folium import ClickForMarker

from sqlalchemy import create_engine, select    # Libraries for DataBase
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from models.user_model import User         # Imports from other files
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required



app = Flask(__name__)
app.secret_key = "za2d345%5"
engine = create_engine("sqlite:///DB/PetHunt.db")
session = Session(engine)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_message = "Для доступа к этой странице необходимо авторизоваться"
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter(User.user_id == user_id).first()

@app.route("/")         #TODO: Main Page
@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=["POST", "GET"])        # register page
def register():
    if flask.request.method == "POST":
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


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        log = request.form['log']
        pas = request.form['pas']
        user = session.execute(select(User).where(User.login == log)).first()
        if user:
            user = user[0]
            #if check_password_hash(user.password_hash, pas):
            if str(user.password) == pas:
                login_user(user)
                flash("Вы успешно вошли!", "success")
                return redirect(url_for('index'))
            else:
                flash("Неверный пароль", "error")
        else:
            flash("Пользователь не найден", "error")

    return render_template('login.html')


@app.route("/add", methods=["POST", "GET"])         # add page
def add():
    mapObj = folium.Map(location=[55.800595, 37.473519], zoom_start=14)
    folium.GeoJson("shukino.geojson").add_to(mapObj)
    mapObj.add_child(ClickForMarker())
    mapObj.get_root().render()
    header = mapObj.get_root().header.render()
    body = mapObj.get_root().html.render()
    script = mapObj.get_root().script.render()
    return render_template("add.html", header=header, body=body, script=script)


# @app.route("/add_start_marker", methods=["POST", "GET"])
# def add_marker():
#     mapObj = folium.Map(location=[55.800595, 37.473519], zoom_start=14)
#     if flask.request.method == "GET":
#         folium.GeoJson("shukino.geojson").add_to(mapObj)
#         mapObj.add_child(ClickForMarker())
#         mapObj.get_root().render()
#         header = mapObj.get_root().header.render()
#         body = mapObj.get_root().html.render()
#         script = mapObj.get_root().script.render()
#     if flask.request.method == "POST":
#         anns = session.query(ann).all()
#         mapObj.save(f'announcements/{len(anns) + 1}_ann/templates/map.html')
#         return redirect('/index')
#     return render_template("start_marker.html", header=header, body=body, script=script)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
