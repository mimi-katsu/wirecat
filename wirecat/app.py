import os
from werkzeug.security import generate_password_hash
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from db import db, User, Post
from config import Config, DevEnv, ProdEnv, Uploads
import secrets
from wirecat.util.catlib import catlib
from sqlalchemy.exc import IntegrityError
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
        # hash method should = pbkdf2:sha256, remove if it doesnt work
        try:
            key = secrets.token_hex(32)
            user = User(username='mimi', first_name='mimi', last_name='???',email = 'mimi@wirecat.org', password = generate_password_hash('123123', method='pbkdf2:sha256'), api_key=generate_password_hash(key, method='pbkdf2:sha256'))
            db.session.add(user)
            db.session.commit()
            with open('./mimi.key', 'w') as f:
                f.write(key)
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
    jwt = JWTManager(app)
    return app

app = create_app()