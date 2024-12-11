import flask        # Libraries for WEB page
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import folium       # Libraries for map
from folium.plugins import MousePosition

from sqlalchemy import create_engine, select    # Libraries for DataBase
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from models.sqlmodels import User         # Imports from other files


app = Flask(__name__)
engine = create_engine("sqlite:///DB/PetHunt.db", echo=True)    # page initial


@app.route("/")         #TODO: Main Page
@app.route("/index")
def home():
    mapObj = folium.Map(location=[55.800595, 37.473519], zoom_start=14)
    folium.GeoJson("shukino.geojson").add_to(mapObj)
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    MousePosition(
        position="topright",
        separator=" | ",
        empty_string="NaN",
        lng_first=True,
        num_digits=20,
        prefix="Coordinates:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(mapObj)
    mapObj.get_root().render()
    header = mapObj.get_root().header.render()
    body = mapObj.get_root().html.render()
    script = mapObj.get_root().script.render()
    return render_template("index.html", header=header, body=body, script=script)


@app.route("/register", methods=["POST", "GET"])        # register page
def register():
    with Session(engine) as session:
        if flask.request.method == "POST":
            log = request.form['login']
            pas = request.form['password']
            fio = request.form['fio']
            phone = request.form['phone']
            ds = request.form['area']
            if log is not None and pas is not None and fio is not None and phone is not None and ds is not None:
                stmt = select(User).where(User.login.in_(["log"]))
                for user in session.scalars(stmt):
                    print(user)
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
        else:
            return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])           # login page
def login():
    if flask.request.method == "POST":
        log = request.form['log']
        pas = request.form['pas']
        print(log, pas)
        with Session(engine) as session:
            user = session.query(User).filter(User.login == log).first()
            print(user.login, user.password)
            if str(user.login) == log and str(user.password) == pas:
                return redirect('/index')
            return render_template('login.html')
    else:
        return render_template("login.html")


@app.route("/add", methods=["POST", "GET"])         # add page
def add():
    if flask.request.method == "POST":
        pass
    return render_template("add.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
