from marshmallow import Schema, fields

class TherapistSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)
    email_found = fields.Str(allow_none=True)
    phone_found = fields.Str(allow_none=True)
    profile_url = fields.Str(allow_none=True)
    extra_info = fields.Dict(allow_none=True)

class ScrapeTaskResultSchema(Schema):
    status = fields.Str(required=True)
    data = fields.List(fields.Nested(TherapistSchema), allow_none=True)
    error = fields.Str(allow_none=True)