from nbewdb import db, User, UserMeta, Author, Post, PostMeta, ApiKeys
from flask import Flask
import secrets
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)

    with app.app_context():
        db.create_all()

        # Creating and adding a new user
        user1 = User(username='John Doe', verfified = False, creation_date='123', first_name="not john", email="123@.com")
        user2 = User(username="maia",perm = 'superadmin', verfified = True, creation_date='1asdasd23', first_name="not miaa", email="1sdasd23@.com")
            
        keys = ApiKeys(user_id = user1.id, key = secrets.token_hex(32), expires='never')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(keys)
        db.session.commit()

        user = User.query.filter_by(username='maia').first()
        author = Author(username=user.username, user_id=user.id, gender='something', about='nothing')
        db.session.add(author)
        db.session.commit()
        other_user = User.query.filter_by(username='John Doe').first()
        key = ApiKeys(user_id=other_user.id, key = secrets.token_hex(32), expires='12123123')
        print(author)
        # Creating and adding a new post
        post1 = Post(author_id=author.id, title='Tasdest', html_content='Testasd title', slug='123123', publish_date='123')
        post2 = Post(author_id=author.id, title='Test', html_content='Test title', slug='1231aaa23', publish_date='123')
        db.session.add(key)
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
        # # Querying posts with a join
        posts = Post.query.join(Author).filter(author.username == 'maia').all()
        user = User.query.filter_by(username='John Doe').first()
        keys = ApiKeys.query.join(User).filter(user.username=='John Doe').first()

        print(user.username)
        print(User.query.all())
        print(posts)
        print(keys.key)


    return app

app = create_app()