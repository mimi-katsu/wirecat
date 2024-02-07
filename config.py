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
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Uploads:
    UPLOADED_PHOTOS_DEST = "uploads"

class Permissions:
    """superadmin, admin, user, author, banned"""
    CAN_POST = ['superadmin', 'admin', 'author']
    SEE_OWN_STATS = ['superadmin', 'admin', 'author']
    SEE_ALL_STATS = ['superadmin', 'admin']
    CAN_CREATE_POST= ['superadmin', 'admin', 'author']
    CAN_PUBLISH = ['admin', 'superadmin', 'admin']
    CAN_DELETE = ['admin', 'superadmin']
    CAN_HIGHLIGHT = ['admin', 'superadmin']
    CAN_REGISTER_USERS = ['admin', 'superadmin']
    CAN_REGISTER_ADMINS = ['superadmin']
    CAN_MAKE_ANNOUNCEMENTS = ['superadmin', 'admin']

class Posts:
    CATEGORIES = ['ctf', 'opinion', 'news', 'site', 'programming', 'homelab', 'guide', 'tool']