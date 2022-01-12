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
from models import db, User, Post
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

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize_with_posts(), users))

    return jsonify(users), 200

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

    new_user = User(email=body['email'], password=body['password'], is_active=body['is_active'])
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

@app.route('/post/<int:post_id>')
def get_post_by_id(post_id):
    post = Post.query.get(post_id)
    if post:
        post = post.serialize()
        return jsonify(post),200
    return jsonify({"mensaje": "Post no encontrado"}), 404



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
