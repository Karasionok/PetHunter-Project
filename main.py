import flask        # Libraries for WEB page
from flask import Flask, render_template, request, redirect

import folium       # Libraries for map

from sqlalchemy import create_engine, select    # Libraries for DataBase
from sqlalchemy.orm import Session

from models.sqlmodels import User         # Imports from other files


app = Flask(__name__)
engine = create_engine("sqlite:///DB/PetHunt.db", echo=True)    # page initial


@app.route("/")         # Main Page
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


@app.route("/register", methods=["POST", "GET"])        # register page
def register():
    if flask.request.method == "POST":
        log = request.form['lg']
        pas = request.form['ps']
        fio = request.form['fio']
        phone = request.form['phone']
        ds = request.form['ds']
        if log is not None and pas is not None:
            print(log, pas, fio, phone, ds)
            with Session(engine) as session:
                usr = User(
                    full_name = fio,
                    login = log,
                    password = pas,
                    phone = phone,
                    district = ds
                )
                session.add(usr)
                session.commit()
        return redirect('/index')
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])           # login page
def login():
    if flask.request.method == "POST":
        log = request.form['log']
        pas = request.form['pas']
        print(log, pas)
        with Session(engine) as session:
            stmt = select(User).where(User.login.in_(["log"]))
            for user in session.scalars(stmt):
                print(user)
        return redirect('/index')
    else:
        return render_template("login.html")


@app.route("/add", methods=["POST", "GET"])         # add page
def add():
    return render_template("add.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
