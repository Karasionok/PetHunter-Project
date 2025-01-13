import os

import flask        # Libraries for WEB page
from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup

import folium       # Libraries for map
from folium import ClickForMarker

from sqlalchemy import create_engine, select    # Libraries for DataBase
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from models.user_model import User         # Imports from other files
from models.announ_model import Annoucement as ann


app = Flask(__name__)
engine = create_engine("sqlite:///DB/PetHunt.db", echo=True)    # page initial
session = Session(engine)


@app.route("/")         #TODO: Main Page
@app.route("/index")
def home():
    return render_template("index.html")


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


@app.route("/proba", methods=["POST", "GET"])
def proba():
    return render_template("SAiti.html")


@app.route("/login", methods=["POST", "GET"])           # login page
def login():
    if flask.request.method == "POST":
        log = request.form['log']
        pas = request.form['pas']
        print(log, pas)
        user = session.query(User).filter(User.login == log).first()
        print(user.login, user.password)
        if str(user.login) == log and str(user.password) == pas:
            return redirect('/index')
        return render_template('login.html')
    else:
        return render_template("login.html")


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
