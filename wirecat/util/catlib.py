import sqlite3
import os
from datetime import datetime
import random
import string
import secrets

class catlib:

        def generate_api_key():
                return secrets.token_hex(32)

        def generate_id(length=12):
                '''create an alphanumeric post id if it doesn't exist already'''
                characters = string.ascii_letters + string.digits 
                random_id = ''.join(random.choice(characters) for _ in range(length))
                return random_id

        def html_image_path():
                now = datetime.now()
                return f'/static/posts/{str(now.year)}/{str(now.month)}/{str(now.day)}'

        def file_save_path():
                now = datetime.now()
                path = os.path.join(f'{os.getcwd()}/wirecat/static/posts/{str(now.year)}/{str(now.month)}/{str(now.day)}')
                os.makedirs(path, exist_ok=True)
                if os.path.exists(path):
                        return path
                else:
                        return None

        def verify_post(post_request):
                #TODO
                #Implement logic for verifying post contents, sanitizing file paths, etc.
                return True
# class Database:
#     def init_db(self):
#         # create connection to database
#         connection = sqlite3.connect("./db/devdb.sqlite")
#         cursor = connection.cursor()
#         #set journal mode for persistence
#         cursor.execute("""PRAGMA journal=WAL""")
#         #create posts table
#         cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
#             post_id TEXT PRIMARY KEY,
#             title TEXT NOT NULL,
#             author TEXT NOT NULL,
#             html_content TEXT NOT NULL,
#             summary TEXT,
#             thumbnail TEXT,
#             publish_date DATETIME NOT NULL,
#             tags TEXT
#         )""")

#         cursor.execute("""CREATE TABLE IF NOT EXISTS users (
#             user_id TEXT PRIMARY KEY,
#             username TEXT NOT NULL,
#             first_name TEXT,
#             last_name TEXT,
#             email TEXT NOT NULL,
#             date_created NOT NULL,
#             favorites TEXT

#         )""")
#         connection.commit()
#         return connection

#     def create_user(self, user:object):
#         conn = self.init_db()
#         cursor = conn.cursor()
#         cursor.execute("""INSTER INTO users (
#             user_id, username, first_name, last_name, email, date_created, favorites, api_key, secret_key, password VALUES (?,?,?,?,?,?,?,?,?,?)""",
#             (user.user_id, user.username, user.first_name, user.last_name, user.email, user.date_created, user.favorites, user.api_key, user.secret_key, user.password))
    
#     def get_user(self, user_name):
#         conn = self.init_db()
#         cursor = conn.cursor()
#         cursor.execute(f""" SELECT * FROM users WHERE user_name ={user_name}""")
#         return cursor.fetchone()

#     def create_post(self, post:object):
#         conn = self.init_db()
#         cursor = conn.cursor()
#         cursor.execute("""INSERT INTO posts (
#             post_id, title, author, html_content, summary, thumbnail, publish_date, tags) VALUES (?,?,?,?,?,?,?,?)""",
#             (post.id, post.title, post.author, post.html_content, post.summary, post.thumbnail, post.publish_date, post.tags))
#         conn.commit()
#         conn.close()

#     def get_recent_posts(self) -> list[object]:
#         conn = self.init_db()
#         cursor = conn.cursor()
#         posts = []
#         cursor.execute("""SELECT * FROM posts ORDER BY publish_date DESC LIMIT 5""")

#         post_raw = cursor.fetchall()
#         for p in post_raw:
#             post = Post(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7])
#             posts.append(post)

#         conn.close()
#         return posts

# db = Database()

# post1 = Post()
# post1.title = "Post 1"
# post1.summary = "This is a summary of post ONE, its just a small amount of text that describes the post"
# post1.author = "Maia"
# post1.html_content = """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur non dolor et libero hendrerit luctus. Pellentesque metus orci, egestas tempus mauris id, ultrices scelerisque arcu. Cras venenatis venenatis massa, vel rutrum dolor laoreet id. Curabitur quis lobortis arcu. Vivamus maximus, sem ac vestibulum molestie, lacus lorem tempor justo, vel mattis dolor diam in ante. Proin ut justo velit. Duis accumsan commodo erat, sit amet molestie mi viverra accumsan. Donec quis fermentum ligula. </p>"""
# db.create_post(post1)

# post2 = Post()
# post2.title = "Post 2"
# post2.summary = "This is a summary of post TWOoowwoo, its just a small amount of text that describes the post"
# post2.author = "Maia"
# post2.html_content = """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur non dolor et libero hendrerit luctus. Pellentesque metus orci, egestas tempus mauris id, ultrices scelerisque arcu. Cras venenatis venenatis massa, vel rutrum dolor laoreet id. Curabitur quis lobortis arcu. Vivamus maximus, sem ac vestibulum molestie, lacus lorem tempor justo, vel mattis dolor diam in ante. Proin ut justo velit. Duis accumsan commodo erat, sit amet molestie mi viverra accumsan. Donec quis fermentum ligula. </p>"""
# db.create_post(post2)

# post3 = Post()
# post3.title = "Post 3"
# post3.summary = "This is a summary of post THREEEE, its just a small amount of text that describes the post"
# post3.author = "Maia"
# post3.html_content = """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur non dolor et libero hendrerit luctus. Pellentesque metus orci, egestas tempus mauris id, ultrices scelerisque arcu. Cras venenatis venenatis massa, vel rutrum dolor laoreet id. Curabitur quis lobortis arcu. Vivamus maximus, sem ac vestibulum molestie, lacus lorem tempor justo, vel mattis dolor diam in ante. Proin ut justo velit. Duis accumsan commodo erat, sit amet molestie mi viverra accumsan. Donec quis fermentum ligula. </p>"""
# db.create_post(post3)

# s = Secrets()
# u = Users()
# user = User()
# user.username = 'mimi'
# user.email = 'mimi@wirecat.org'
# user.first_name = 'mimi'
# user.password = s.sha_256_hash('password123!')
# user.api_key, user.secret_key = s.new_api_key()

# print(user.username, user.api_key)

# catlib.make_current_dir_posts()