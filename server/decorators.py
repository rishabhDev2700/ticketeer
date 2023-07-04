from functools import wraps
import jwt
from flask import request, current_app
from server.models import User,db 

def token_authentication(func):
    @wraps(func)
    def token_validation(*args,**kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return {
                'message':'Authentication token missing',
                'data':None,
                'error':'Unauthorized'
            },401
        try:
            data = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
            user = db.get_or_404(User,data['user_id'])
            if user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
                }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
        return func(user,*args,**kwargs)
    return token_validation