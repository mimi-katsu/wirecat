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
            user1 = User(username='mimi', first_name='mimi', last_name='???',email = 'mimi@wirecat.org', verified = True, creation_date='2023/12/1',password = generate_password_hash('12345', method='pbkdf2:sha256'), perm='superadmin')
            user2 = User(username='alexandra', first_name='alexandra', last_name='nesta',email = 'alexandra@yahoo.com', verified = True, creation_date='2024/1/17',password = generate_password_hash('123123', method='pbkdf2:sha256'), perm='author')
            user3 = User(username='jimbob', first_name='jim', last_name='bob',email = 'jimbob@wirecat.org', verified = True, creation_date='2024/2/25',password = generate_password_hash('123123', method='pbkdf2:sha256'), perm='user')
            user4 = User(username='stacy', first_name='stacy', last_name='mayo',email = 'stacy@google.org', verified = True, creation_date='2024/4/12',password = generate_password_hash('123123', method='pbkdf2:sha256'), perm='admin')

            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.add(user4)

            db.session.commit()

            user1 = User.query.filter_by(username = 'mimi').first()
            user2 = User.query.filter_by(username = 'alexandra').first()
            user3 = User.query.filter_by(username = 'jimbob').first()
            user4 = User.query.filter_by(username = 'stacy').first()

            profile1 = Profile(user_id=user1.id, gender='female', about='''Mreeow. I've been doing sus stuff online for 15 years''', dob='1111/11/11')
            profile2 = Profile(user_id=user2.id, gender='male', about='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vel ligula non massa aliquet malesuada. Pellentesque ultrices facilisis metus, eu consectetur dui.', dob='1990/11/23')
            profile3 = Profile(user_id=user3.id, gender='NB', about='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vel ligula non massa aliquet malesuada. Pellentesque ultrices facilisis metus, eu consectetur dui.', dob='2002/6/19')
            profile4 = Profile(user_id=user4.id, gender='female', about='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vel ligula non massa aliquet malesuada. Pellentesque ultrices facilisis metus, eu consectetur dui.', dob='2023/8/7')

            db.session.add(profile1)
            db.session.add(profile2)
            db.session.add(profile3)
            db.session.add(profile4)

            mimi_key = secrets.token_hex(32)
            alexandra_key = secrets.token_hex(32)
            jimbob_key = secrets.token_hex(32)
            stacy_key = secrets.token_hex(32)

            newkey1 = ApiKeys(user_id = user1.id, key = generate_password_hash(mimi_key, method='pbkdf2:sha256'), expires='never')
            newkey2 = ApiKeys(user_id = user2.id, key = generate_password_hash(alexandra_key, method='pbkdf2:sha256'), expires='234')
            newkey3 = ApiKeys(user_id = user3.id, key = generate_password_hash(jimbob_key, method='pbkdf2:sha256'), expires='234123')
            newkey4 = ApiKeys(user_id = user4.id, key = generate_password_hash(stacy_key, method='pbkdf2:sha256'), expires='123asdasd')

            db.session.add(newkey1)
            db.session.add(newkey2)
            db.session.add(newkey3)
            db.session.add(newkey4)

            db.session.commit()
            with open('./mimi.key', 'w') as f:
                f.write(mimi_key)
            with open('./alexandra.key', 'w') as f:
                f.write(alexandra_key)
            with open('./jimbob.key', 'w') as f:
                f.write(jimbob_key)
            with open('./stacy.key', 'w') as f:
                f.write(stacy_key)

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
