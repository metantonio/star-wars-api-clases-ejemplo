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
from models import db, User, People, Favorite_People
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
bcrypt = Bcrypt(app)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if "email" not in body:
        raise APIException('You need to specify the email', status_code=400)
    if "password" not in body:
        raise APIException('You need to specify the password', status_code=400)

    user = User.query.filter_by(email=body['email']).first()

    if not user:
        raise APIException('User or password are incorrect', status_code=400)
    if user and not bcrypt.check_password_hash(user.password, body['password']):
        raise APIException('User or password are incorrect', status_code=400)

    access_token = create_access_token(identity=body["email"])
    return jsonify({"access_token":access_token})


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    people = list(map(lambda character: character.serialize(), people))

    return jsonify(people), 200

@app.route('/favorite/people', methods=['GET'])
def get_all_people_favorite():
    people = Favorite_People.query.all()
    people = list(map(lambda character: character.serialize(), people))

    return jsonify(people), 200

@app.route('/users', methods=['POST'])
def create_new_user():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if "email" not in body:
        raise APIException('You need to specify the email', status_code=400)
    if "password" not in body:
        raise APIException('You need to specify the password', status_code=400)
    if "is_active" not in body:
        raise APIException('You need to specify the is_active', status_code=400)
    
    hashed_password = bcrypt.generate_password_hash(body["password"])

    new_user = User(email=body['email'], password=hashed_password, is_active=body['is_active'])
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

@app.route('/favorite/people', methods=['POST'])
def create_new_favorite_people():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if "user_id" not in body:
        raise APIException('You need to specify the user_id', status_code=400)
    if "people_id" not in body:
        raise APIException('You need to specify the people_id', status_code=400)

    new_favorite_people = Favorite_People(user_id=body['user_id'], people_id=body["people_id"])
    
    db.session.add(new_favorite_people)
    db.session.commit()

    return jsonify({"mensaje": "Favorito creado exitosamente"}), 201

@app.route('/people/<int:people_id>')
@jwt_required()
def get_people_by_id(people_id):
    user_email = get_jwt_identity()
    people = People.query.get(people_id)
    print(get_jwt_identity())
    if people:
        people_serialize = post.serialize()
        return jsonify(people_serialize),200
    return jsonify({"mensaje": "Post no encontrado"}), 404



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
