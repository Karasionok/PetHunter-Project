import flask
from flask import Flask, render_template, request, redirect
import folium
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from sqlalchemy import *
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB/PetHunt.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    login = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    district = db.Column(db.String, nullable=False)


@app.route("/")
@app.route("/index")
def home():
    mapObj = folium.Map(location=[55.800595, 37.473519], zoom_start=14)
    folium.GeoJson("shukino.geojson").add_to(mapObj)
    popup1 = folium.LatLngPopup()
    mapObj.add_child(popup1)
    mapObj.get_root().render()
    header = mapObj.get_root().header.render()
    body = mapObj.get_root().html.render()
    script = mapObj.get_root().script.render()
    return render_template("index.html", header=header, body=body, script=script)


@app.route("/register", methods=["POST", "GET"])
def register():
    if flask.request.method == "POST":
        log = request.form['lg']
        pas = request.form['ps']
        fio = request.form['fio']
        phone = request.form['phone']
        ds = request.form['ds']
        if log != '' and pas != '':
            print(log, pas, fio, phone, ds)
            usr = User(login=log, password=pas, full_name=fio, phone=phone, district=ds)
            db.session.add(usr)
            db.session.commit()
        return redirect('/index')
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        log = request.form['log']
        pas = request.form['pas']
        print(log, pas)
        return redirect('/index')
    else:
        return render_template("login.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
