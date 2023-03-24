"""
Views for authentication/authorization
"""
import datetime

from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from app.models.users import User


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        user_id = user.id
        return {'id': str(user_id)}


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(username=body.get('username'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'error': 'Email or password invalid'}, 401

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200
