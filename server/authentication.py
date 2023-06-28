from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from server.models import User, db

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
    except:
        response = {'status':'created','name':first_name+' '+last_name}
        return jsonify(response)
    return jsonify()

@authentication.post('/login')
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    password_hash = user.password
    if check_password_hash(password_hash,password):
        pass
    response = {'message':'Invalid credentials!'}
    return jsonify(response)

@authentication.post('/logout')
def logout_user():
    
    return jsonify()