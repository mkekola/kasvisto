import secrets, sqlite3
from flask import Flask
from flask import abort, make_response, redirect, render_template, request, session
import config
import plants
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    all_plants = plants.get_plants()
    return render_template("index.html", plants=all_plants)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_plants = users.get_plants(user_id)
    return render_template("show_user.html", user=user, plants=user_plants)

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
    categories = plants.get_category_by_id(plant_id)
    if not categories:
        categories = []
    else:
        categories = [category["category"] for category in categories]
    comments = plants.get_comments(plant_id)
    images = plants.get_images(plant_id)
    return render_template("show_plant.html", plant=plant, categories=categories, comments=comments, images=images)

@app.route("/images/<int:plant_id>", methods=["GET", "POST"])
def edit_images(plant_id):
    require_login()
    check_csrf()
    plant = plants.get_plant(plant_id)
    if not plant:
        abort(404)
    if plant["user_id"] != session["user_id"]:
        abort(403)

    images = plants.get_images(plant_id)
    return render_template("images.html", plant=plant, images=images)

@app.route("/image/<int:image_id>.png")
def show_image(image_id):
    image = plants.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/new_plant", methods=["POST"])
def new_plant():
    require_login()
    check_csrf()
    categories = plants.get_categories()
    return render_template("new_plant.html", categories=categories)


@app.route("/create_plant", methods=["POST"])
def create_plant():
    require_login()
    check_csrf()
    plant_name = request.form["plant_name"]
    if not plant_name or len(plant_name) > 50:
        abort(403)
    light = request.form["light"]
    if not light:
        abort(403)
    care_info = request.form["care_info"]
    if not care_info or len(care_info) > 500:
        abort(403)
    user_id = session["user_id"]

    selected_categories = []
    categories = request.form.getlist("categories")

    if not categories:
        abort(403)

    for cat in categories:
        selected_categories.append(cat)

    plants.add_plant(plant_name, light, care_info, user_id, selected_categories)

    return redirect("/")

@app.route("/create_comment/<int:plant_id>", methods=["POST"])
def create_comment(plant_id):
    require_login()
    check_csrf()
    content = request.form["comment"]
    if not content or len(content) > 500:
        abort(403)
    user_id = session["user_id"]
    plants.add_comment(plant_id, user_id, content)
    return redirect("/plant/" + str(plant_id))


@app.route("/edit_plant/<int:plant_id>", methods=["POST"])
def edit_plant(plant_id):
    require_login()
    check_csrf()
    plant = plants.get_plant(plant_id)
    if not plant:
        abort(404)
    if plant["user_id"] != session["user_id"]:
        abort(403)
    all_categories = plants.get_categories()
    plant_categories = plants.get_category_by_id(plant_id)
    if not plant_categories:
        plant_categories = []
    else:
        plant_categories = [category["category"] for category in plant_categories]
    return render_template("edit_plant.html", plant=plant, all_categories=all_categories, plant_categories=plant_categories)

@app.route("/add_image/<int:plant_id>", methods=["POST"])
def add_image(plant_id):
    require_login()
    check_csrf()
    plant_id = request.form["plant_id"]
    plant = plants.get_plant(plant_id)
    if not plant:
        abort(404)
    if plant["user_id"] != session["user_id"]:
        abort(403)

    file = request.files["image"]
    if not file.filename.endswith(".png"):
        return "VIRHE: vain .png kuvat sallittu"

    image = file.read()
    if len(image) > 2 * 1024 * 1024:
        return "VIRHE: kuvan on oltava enintään 2 Mt"
    
    plants.add_image(plant_id, image)
    return redirect("/images/" + str(plant_id))

@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()

    plant_id = request.form["plant_id"]
    plant = plants.get_plant(plant_id)
    if not plant:
        abort(404)
    if plant["user_id"] != session["user_id"]:
        abort(403)

    for image_id in request.form.getlist("image_id"):
        plants.remove_image(plant_id, image_id)

    return redirect("/images/" + str(plant_id))


@app.route("/update_plant", methods=["POST"])
def update_plant():
    require_login()
    plant_id = request.form["plant_id"]
    plant = plants.get_plant(plant_id)
    if not plant:
        abort(404)
    if plants.get_plant(plant_id)["user_id"] != session["user_id"]:
        abort(403)
    plant_name = request.form["plant_name"]
    if not plant_name or len(plant_name) > 50:
        abort(403)
    light = request.form["light"]
    if not light:
        abort(403)
    care_info = request.form["care_info"]
    if not care_info or len(care_info) > 500:
        abort(403)
    all_categories = [category["category"] for category in plants.get_categories()]
    categories = []
    for category in request.form.getlist("categories"):
        if category in all_categories:
            categories.append(category)
    plants.update_plant(plant_id, plant_name, light, care_info, categories)
    return redirect("/plant/" + str(plant_id))


@app.route("/delete_plant/<int:plant_id>", methods=["GET", "POST"])
def delete_plant(plant_id):
    require_login()
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
        return redirect("/plant/" + str(plant_id))


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create_user():
    username = request.form["username"]
    if not username or len(username) > 20:
        return "VIRHE: tunnus on liian pitkä tai tyhjä"
    password1 = request.form["password1"]
    if not password1:
        return "VIRHE: salasana on tyhjä"
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        if not username:
            return "VIRHE: tunnus on tyhjä"
        password = request.form["password"]
        if not password:
            return "VIRHE: salasana on tyhjä"

        user_id = users.authenticate_user(username, password)

        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            session["username"] = username
            return redirect("/")
        return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
