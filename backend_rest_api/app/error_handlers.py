import traceback
from flask import Flask, jsonify
from app.views.file_helper import FileTypeNotSupported


class ContentNotFound(Exception):
    """To return HTTP Response 204"""
    pass


def setup_error_handlers(app: Flask):
    def make_response(msg: str, status_code: int):
        resp = jsonify({"msg": msg})
        return resp, status_code

    @app.errorhandler(Exception)
    def error_handler_exception(error):
        print(traceback.format_exc())
        return make_response("Unexpected error occurred", 500)

    @app.errorhandler(ContentNotFound)
    def content_not_found_exception(error):
        return make_response("Content not found", 204)

    @app.errorhandler(FileTypeNotSupported)
    def file_type_not_supported(error):
        return make_response("File type not supported", 405)
