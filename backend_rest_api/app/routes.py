from flask import Flask
from flask_restful import Api

from app.views.auth import SignupApi, LoginApi
from app.views.file import FileUpload, FileRetrieve


def add_resources(app: Flask):
    api = Api(app)

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

    api.add_resource(FileUpload, '/v1/table')
    api.add_resource(FileRetrieve, '/v1/table/<string:file_id>')
