import os
from flask import Flask, render_template
from db import db, User, Post, UserMeta, PostMeta

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(app.instance_path, 'cat.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    @app.errorhandler(404)
    def page_not_found(e):
        # Note that we set the 404 status explicitly
        return render_template('404.html'), 404

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
        # user1 = User(username='maia1', email = 'test1@test.com', password = '123123')
        # user2 = User(username='maia2', email = 'test2@test.com', password = '123123')
        # user3 = User(username='maia3', email = 'test3@test.com', password = '123123')
        # db.session.add(user1)
        # db.session.add(user2)
        # db.session.add(user3)
        # db.session.commit()
        # u = db.session.execute(db.select(user2.user_id))
        # print(u)
        # print(User.query.all())
        # # print(u.username)
        # # User.query.filter_by(username = user1.username) 
        # print('1')
        # print(User.query.get(user2.user_id))
        # print('1')
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

    from .routes import wc
    app.register_blueprint(wc)

    return app

app = create_app()