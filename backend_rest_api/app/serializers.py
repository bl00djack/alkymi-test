from marshmallow import Schema, fields, EXCLUDE


class TemporalSerializer(Schema):
    class Meta:
        unknown = EXCLUDE

    row = fields.Int()
    column = fields.Int()
    startIdx = fields.Int()
    endIdx = fields.Int()
    text = fields.String()
    temporal = fields.String()


class DataFileSerializer(Schema):
    file_id = fields.UUID()
    file_name = fields.String()
    file_status = fields.String()
    has_header_row = fields.Bool()
    header = fields.List(fields.String())
    rows = fields.List(fields.List(fields.Raw()))
    temporals = fields.List(fields.Nested(TemporalSerializer))
