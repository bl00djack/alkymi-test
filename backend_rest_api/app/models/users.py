from mongoengine import Document, StringField
from flask_bcrypt import generate_password_hash, check_password_hash


class User(Document):
    meta = {"collection": "users"}

    username = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
