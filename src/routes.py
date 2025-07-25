from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, Planet, People, Favorite

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///starwars.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
Migrate(app, db)
CORS(app)


@app.route("/")
def home():
    return jsonify({"ok": True})

# ---------------- PEOPLE ----------------


@app.route("/people", methods=["GET"])
def get_people():
    characters = People.query.all()
    return jsonify([c.serialize() for c in characters])


@app.route("/people/<int:people_id>", methods=["GET"])
def get_one_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 400
    return jsonify(person.serialize())

# --- PLANETS ----


@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets])


@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 400
    return jsonify(planet.serialize())


# -- USERS ---

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users])


@app.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([f.serialize() for f in favorites])

# ---------------- FAVORITES ----------------


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_fav_planet(planet_id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Planet favorited!"}), 200


@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_fav_person(people_id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    fav = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Person favorited!"}), 200


@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def remove_fav_planet(planet_id):
    user_id = request.json.get("user_id")
    fav = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"error": "Favorite not found"}), 400
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Planet unfavorited"})


@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def remove_fav_person(people_id):
    user_id = request.json.get("user_id")
    fav = Favorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    if not fav:
        return jsonify({"error": "Favorite not found"}), 400
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Person unfavorited"})
