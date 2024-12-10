import flask        # Libraries for WEB page
from flask import Flask, render_template, request, redirect

import folium       # Libraries for map

from sqlalchemy import create_engine, select    # Libraries for DataBase
from sqlalchemy.orm import Session

from models.sqlmodels import User         # Imports from other files


app = Flask(__name__)
engine = create_engine("sqlite:///DB/PetHunt.db", echo=True)    # page initial


@app.route("/")         #TODO: Main Page
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
            user_log = session.query(User.login).filter(User.login == log).first()
            user_pas = session.query(User.password).filter(User.login == log).first()
            print(str(user_log[0]), str(user_pas[0]))
            if str(user_log[0]) == log and str(user_pas[0]) == pas:
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
