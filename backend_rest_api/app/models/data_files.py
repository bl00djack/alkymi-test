"""
Model for DataFile objects
"""
from uuid import uuid4
from mongoengine.fields import UUIDField
from mongoengine import (
    Document, EmbeddedDocument, EmbeddedDocumentField, StringField,
    BooleanField, ListField, IntField, ReferenceField)


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
