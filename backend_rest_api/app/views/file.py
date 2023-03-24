"""
Views for file upload and file retrieve
"""
import io
import csv
from werkzeug.utils import secure_filename
from mongoengine import DoesNotExist

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.data_files import DataFile
from app.models.users import User
from app.serializers import DataFileSerializer
from app.error_handlers import ContentNotFound
from app.views.file_helper import FileHelperFactory


class FileUpload(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        has_header_row = request.args.get('headerRow', False) == 'true'
        f = request.files.get('file')
        # Extracting uploaded file name
        data_filename = secure_filename(f.filename)
        file_extension = data_filename.split('.')[1]
 
        # f.save(os.path.join(Config.UPLOAD_FOLDER, data_filename))
        file_reader = FileHelperFactory.get_reader(f, file_extension)
        header, rows = file_reader.get_data(has_header_row)

        user = User.objects.get(id=user_id)
        data_file = DataFile(
            file_name=data_filename,
            file_status='processing',
            has_header_row=has_header_row,
            header=header,
            rows=rows,
            added_by=user
        )
        data_file.save()
 
        return {
            'file_id': str(data_file._id),
            'status': data_file.file_status
        }


class FileRetrieve(Resource):
    @jwt_required()
    def get(self, file_id):
        try:
            data_file = DataFile.objects.get(_id=file_id)
        except DoesNotExist:
            raise ContentNotFound

        serialized_data_file = DataFileSerializer().dump(data_file)
        return {
            'header': serialized_data_file['header'],
            'rows': serialized_data_file['rows'],
            'temporals': serialized_data_file['temporals'],
        }
