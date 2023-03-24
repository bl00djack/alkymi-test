import os


class Config:
    class STANFORDAPI:
        client_secret = os.environ.get("STANFORD_CLIENT_SECRET", "WbB1N1VMN8f0_c6QKaWpWCfZCMpWuUP8Xgir-y9aZt551cMUoc5vb_0TV6XDC0AS")
        client_id = os.environ.get("STANFORD_CLIENT_ID", "VZouYIRkBdYcho9uHjCqBdwpZAuodJSG")

    class AUTH:
        JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", 'dev-secret')
