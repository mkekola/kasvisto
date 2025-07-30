import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import plants as plants

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    all_plants = plants.get_plants()
    return render_template("index.html", plants=all_plants)


@app.route("/find_plant")
def find_plant():
    query = request.args.get("query")
    if query:
        results = plants.find_plants(query)
    else:
        query = ""
        results = []
    return render_template("find_plant.html", query=query, results=results)


@app.route("/plant/<int:plant_id>")
def show_plant(plant_id):
    plant = plants.get_plant(plant_id)
    if not plant:
        abort(404)
    return render_template("show_plant.html", plant=plant)


@app.route("/new_plant")
def new_plant():
    return render_template("new_plant.html")


@app.route("/create_plant", methods=["POST"])
def create_plant():
    plant_name = request.form["plant_name"]
    light = request.form["light"]
    care_info = request.form["care_info"]
    user_id = session["user_id"]

    plants.add_plant(plant_name, light, care_info, user_id)

    return redirect("/")


@app.route("/edit_plant/<int:plant_id>")
def edit_plant(plant_id):
    plant = plants.get_plant(plant_id)
    if not plant:
        abort(404)
    if plant["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_plant.html", plant=plant)


@app.route("/update_plant", methods=["POST"])
def update_plant():
    plant_id = request.form["plant_id"]
    plant = plants.get_plant(plant_id)
    if not plant:
        abort(404)
    if plants.get_plant(plant_id)["user_id"] != session["user_id"]:
        abort(403)
    plant_name = request.form["plant_name"]
    light = request.form["light"]
    care_info = request.form["care_info"]

    plants.update_plant(plant_id, plant_name, light, care_info)

    return redirect("/plant/" + str(plant_id))


@app.route("/delete_plant/<int:plant_id>", methods=["GET", "POST"])
def delete_plant(plant_id):
    if request.method == "GET":
        plant = plants.get_plant(plant_id)
        if not plant:
            abort(404)
        if plant["user_id"] != session["user_id"]:
            abort(403)
        return render_template("delete_plant.html", plant=plant)

    if request.method == "POST":
        if "delete" in request.form:
            plants.delete_plant(plant_id)
            return redirect("/")
        else:
            return redirect("/plant/" + str(plant_id))


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu" + \
           "<br><a href='/login'>Kirjaudu sisään</a>"



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")
