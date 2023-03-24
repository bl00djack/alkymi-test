import os


class Config:
    class DB:
        MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
        MONGO_USER = os.environ.get('MONGO_USER')
        MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    class STANFORDAPI:
        client_secret = os.environ.get("STANFORD_CLIENT_SECRET", "")
        client_id = os.environ.get("STANFORD_CLIENT_ID", "")

    class AUTH:
        JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", 'dev-secret')
