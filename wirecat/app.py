import os
from flask import Flask
from db import db, User, Post, UserMeta, PostMeta

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    print(os.path.join(app.instance_path, 'cat.sqlite'))
    app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        print('1')
        db.create_all()
        user1 = User(username='maia1', email = 'test1@test.com', password = '123123')
        user2 = User(username='maia2', email = 'test2@test.com', password = '123123')
        user3 = User(username='maia3', email = 'test3@test.com', password = '123123')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        u = db.session.execute(db.select(user2.user_id))
        print(u)
        print(User.query.all())
        # print(u.username)
        # User.query.filter_by(username = user1.username) 
        print('1')
        print(User.query.get(user2.user_id))
        print('1')

    return app

app = create_app()

from wirecat import routes
