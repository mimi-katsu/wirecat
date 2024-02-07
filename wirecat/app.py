import os
import secrets
from getpass import getpass
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from wirecat.db import db, User, Post, PostMeta, UserMeta, ApiKeys, Profile
from config import Config, DevEnv, ProdEnv, Uploads, Permissions, Posts
from wirecat.util.catlib import catlib

UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = {'txt','png', 'jpg', 'jpeg', 'gif', 'md'}

def create_app(test_config=None):
    # create and configure the app
    env = os.environ.get("WIRECAT-ENV")
    if not env:
        env = 'dev'

    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config.from_object(Config())
    app.config.from_object(Uploads())
    app.config.from_object(Config())
    app.config.from_object(Permissions())
    app.config.from_object(Posts())
    app.config['CACHE_TYPE'] = 'simple'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    if env == 'dev':
        app.config.from_object(DevEnv())
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'cat.sqlite')

    elif env == 'production':
        app.config.from_object(ProdEnv())

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        db.create_all()
        try:
            default_user = User.query.filter_by(username="wirecat-admin").first()
            if not default_user:
                admin_pass = getpass("Please enter a password for the wirecat-admin user:\n")

                default_user = User(username='wirecat-admin', first_name='wirecat-admin', last_name='?',email = 'wirecat-admin@wirecat.org', verified = True, creation_date='2023/12/1',password = generate_password_hash(admin_pass, method='pbkdf2:sha256'), perm='superadmin')
                db.session.add(default_user)
                db.session.commit()
                default_user = User.query.filter_by(username = 'wirecat-admin').first()
                profile = Profile(user_id=default_user.id, gender='?', about='Mreeow.', dob='1111/11/11')
                db.session.add(profile)
                wirecat_admin_key = secrets.token_hex(32)
                newkey = ApiKeys(user_id = default_user.id, key = generate_password_hash(wirecat_admin_key, method='pbkdf2:sha256'), expires='never')
                db.session.add(newkey)
                db.session.commit()
                with open('./wirecat-admin.key', 'w') as f:
                    f.write(wirecat_admin_key)

        except IntegrityError:
            print(' * Default user already exists')

        except ValueError as e:
            print(e)


    # Set custom 404 template
    @app.errorhandler(404)
    def page_not_found(e):
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
    #Force a redirect to login page when JWT token is expired or doesnt exist. other wise Default returns json
    @jwt.unauthorized_loader
    def unauthorized_callback(error_string):
        return redirect(url_for('wirecat.login'))

    return app

app = create_app()
