import os

class Config(object):
    JWT_TOKEN_LOCATION = ['cookies']

class DevEnv:
    SECRET_KEY = 'dev'
    JWT_SECRET_KEY = 'dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdEnv:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'mysql://127.0.0.1:3306'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Uploads:
    UPLOADED_PHOTOS_DEST = "uploads"