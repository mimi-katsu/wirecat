import os

class Config(object):
    JWT_TOKEN_LOCATION = ['cookies']

class DevEnv:
    JWT_SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'cat.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdEnv:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'mysql://127.0.0.1:3306'
    SQLALCHEMY_TRACK_MODIFICATIONS = False