import os
from werkzeug.security import generate_password_hash
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from db import db, User, Post
from config import Config, DevEnv, ProdEnv, Uploads
import secrets
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
        # key = secrets.token_hex(32)
        # print(key)
        # user = User(username='mimi', first_name='mimi', last_name='???',email = 'mimi@wirecat.org', password = generate_password_hash('123123'), api_key=generate_password_hash(key))
        # db.session.add(user)
        # db.session.commit()
        # u = db.session.execute(db.select(user.user_id))
        # post1 = Post(
        # title = "Post 1",
        # summary = "This is a summary of post ONE, its just a small amount of text that describes the post",
        # author = "Maia",
        # html_content = """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur non dolor et libero hendrerit luctus. Pellentesque metus orci, egestas tempus mauris id, ultrices scelerisque arcu. Cras venenatis venenatis massa, vel rutrum dolor laoreet id. Curabitur quis lobortis arcu. Vivamus maximus, sem ac vestibulum molestie, lacus lorem tempor justo, vel mattis dolor diam in ante. Proin ut justo velit. Duis accumsan commodo erat, sit amet molestie mi viverra accumsan. Donec quis fermentum ligula. </p>""",

        # )
        # post2 = Post(
        # title = "Post 2",
        # summary = "This is a summary of post TWOoowwoo, its just a small amount of text that describes the post",
        # author = "Maia",
        # html_content = """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur non dolor et libero hendrerit luctus. Pellentesque metus orci, egestas tempus mauris id, ultrices scelerisque arcu. Cras venenatis venenatis massa, vel rutrum dolor laoreet id. Curabitur quis lobortis arcu. Vivamus maximus, sem ac vestibulum molestie, lacus lorem tempor justo, vel mattis dolor diam in ante. Proin ut justo velit. Duis accumsan commodo erat, sit amet molestie mi viverra accumsan. Donec quis fermentum ligula. </p>""",
        # )

        # post3 = Post(
        # title = "Post 3",
        # summary = "This is a summary of post THREEEE, its just a small amount of text that describes the post",
        # author = "Maia",
        # html_content = """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur non dolor et libero hendrerit luctus. Pellentesque metus orci, egestas tempus mauris id, ultrices scelerisque arcu. Cras venenatis venenatis massa, vel rutrum dolor laoreet id. Curabitur quis lobortis arcu. Vivamus maximus, sem ac vestibulum molestie, lacus lorem tempor justo, vel mattis dolor diam in ante. Proin ut justo velit. Duis accumsan commodo erat, sit amet molestie mi viverra accumsan. Donec quis fermentum ligula. </p>""",
        # )

        # db.session.add(post1)
        # db.session.add(post2)
        # db.session.add(post3)
        # db.session.commit()

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