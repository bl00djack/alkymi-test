from uuid import uuid4
from mongoengine.fields import UUIDField
from mongoengine import (
    Document, EmbeddedDocument, EmbeddedDocumentField, StringField,
    BooleanField, ListField, IntField, ReferenceField)

from flask_bcrypt import generate_password_hash, check_password_hash


class User(Document):
    meta = {"collection": "users"}

    username = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Temporal(EmbeddedDocument):
    row = IntField()
    column = IntField()
    startIdx = IntField()
    endIdx = IntField()
    text = StringField()
    temporal = StringField()


class DataFile(Document):
    meta = {"collection": "data_files"}
    file_status_choices = [('processing', 'processing'), ('finished', 'finished')]

    _id = UUIDField(default=uuid4, binary=False)
    file_name = StringField()
    added_by = ReferenceField('User', required=True)
    file_status = StringField(choices=file_status_choices)
    lock = BooleanField(default=False)
    has_header_row = BooleanField()
    header = ListField(StringField())
    rows = ListField(ListField())
    temporals = ListField(EmbeddedDocumentField("Temporal"))
