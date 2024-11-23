import flask
from flask import Flask, render_template, request, redirect
import folium


app = Flask(__name__)

@app.route("/")
@app.route("/index")
def home():
    mapObj = folium.Map(location=[55.800595, 37.473519], zoom_start=14)
    folium.GeoJson("shukino.geojson").add_to(mapObj)
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
        print(log, pas, fio, phone, ds)
        return redirect('/index')
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        log = request.form['lg']
        pas = request.form['ps']
        print(log, pas)
        return redirect('/index')
    else:
        return render_template("login.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
