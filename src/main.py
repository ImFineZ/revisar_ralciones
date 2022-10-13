"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Peoples, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.filter().all()
    result = list(map(lambda user: user.serialize(), users))
    response_body = {
        "Usuarios": result,
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route("/people", methods=["GET"])
def get_peoples():
    peoples = Peoples.query.filter().all()
    result = list(map(lambda people: people.serialize(), peoples))
    response_body = {
        "Usuarios": result,
        "msg": "Hello, this is your GET /people response "
    }
    return  jsonify(response_body),200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    people = Peoples.query.get(people_id)
    response_body = {
        "Usuarios": result,
        "msg": "Hello, this is your GET /people response individual "
    }
    return jsonify(response_body),200

@app.route("/planet", methods=["GET"])
def get_planets():
    planets = Planets.query.filter().all()
    result = list(map(lambda planet: planet.serialize(), planets))
    response_body = {
        "Usuarios": result,
        "msg": "Hello, this is your GET /planet response "
    }
    return  jsonify(response_body),200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    response_body = {
        "Usuarios": result,
        "msg": "Hello, this is your GET /planet response individual"
    }
    return  jsonify(response_body),200

@app.route("/favorites", methods=["GET"])
def get_favorites():
    favorites = Favorites.query.filter().all()
    result = list(map(lambda favorite: favorite.serialize(), favorites))
    response_body = {
        "Usuarios": result,
        "msg": "Hello, this is your GET /favorites response "
    }
    return  jsonify(response_body),200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
