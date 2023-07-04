from flask import Blueprint, current_app, jsonify, request
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from server.decorators import token_authentication
from server.models import User, db
import jwt
authentication = Blueprint('auth', __name__, url_prefix='/auth')

@authentication.post('/register')
def register_user():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    password_hash = generate_password_hash(password=password)
    try:
        user = User(first=first_name,last=last_name,email=email,password=password_hash)
        db.session.add(user)
        db.session.commit()
        response = {'status':'created','name':first_name+' '+last_name}
    except Exception as e:
        response = {'status':'failed','message':f'unable to register the user *{e}'}
    return jsonify(response)

@authentication.post('/login')
def login_user():
    data = request.get_json()
    if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    password_hash = user.password
    if check_password_hash(password_hash,password):
        token = jwt.encode(
                    {"user_id": str(user.id)},
                    current_app.config["SECRET_KEY"],
                    algorithm="HS256")
        user_token = {'token':token,'email':user.email,'first_name':user.first, 'last_name':user.last}
        return user_token
    response = {'message':'Invalid credentials!'}
    return jsonify(response)


@authentication.post('/logout')
@token_authentication
def logout_user():    
    return jsonify()