import os
import secrets

from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from db import db, User, Post, PostMeta, UserMeta, ApiKeys, Profile
from config import Config, DevEnv, ProdEnv, Uploads
from wirecat.util.catlib import catlib

UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = {'txt','png', 'jpg', 'jpeg', 'gif', 'md'}

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config.from_object(DevEnv())
    app.config.from_object(Config())
    app.config.from_object(Uploads())
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'cat.sqlite')
    app.config['CACHE_TYPE'] = 'simple'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        db.create_all()
        try:
            mimi_key = secrets.token_hex(32)
            user = User(username='mimi', first_name='mimi', last_name='???',email = 'mimi@wirecat.org', verified = True, creation_date='123',password = generate_password_hash('123123', method='pbkdf2:sha256'), perm='superadmin')
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(username = 'mimi').first()
            profile = Profile(user_id=user.id, gender='something', about='nothing', dob='1111/11/11')
            db.session.add(profile)
            newkey = ApiKeys(user_id = user.id, key = generate_password_hash(mimi_key, method='pbkdf2:sha256'), expires='never')
            db.session.add(newkey)
            db.session.commit()
            key = ApiKeys.query.filter_by(user_id = user.id).first()
            with open('./mimi.key', 'w') as f:
                f.write(mimi_key)
        except IntegrityError:
            print("default user already exists")


    # Set custom 404 template
    @app.errorhandler(404)
    def page_not_found(e):
        # Note that we set the 404 status explicitly
        return render_template('404.html'), 404

    # register main routes blueprint
    from .routes import wc
    app.register_blueprint(wc)
    #register api blueprint
    from .api import wc_api
    app.register_blueprint(wc_api)
    #register auth blueprint
    from .auth import wc_auth
    app.register_blueprint(wc_auth)
    #init JWT token manager
    jwt = JWTManager(app)
    cache = Cache(app)
    cache.init_app(app)
    app.cache = cache
    #Force a redirect to login page when JWT token is expired or doesnt exist. Default returns json
    @jwt.unauthorized_loader
    def unauthorized_callback(error_string):
        return redirect(url_for('wirecat.login'))

    return app

app = create_app()
