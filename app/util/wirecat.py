import sqlite3
import os
from app.util.posts import Post

class WireCat:
    def __init__(self):
        self.db = Database()

class Database:
    def init_db(self):
        # create connection to database
        connection = sqlite3.connect("./db/devdb.sqlite")
        cursor = connection.cursor()

        #set journal mode for persistence
        cursor.execute("""PRAGMA journal=WAL""")
        #create posts table
        cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            author TEXT NOT NULL,
            html_content TEXT NOT NULL,
            publish_date DATETIME NOT NULL,
            tags TEXT
        )""")
        connection.commit()

        return connection

    def create_post(self, post:object):
        
        conn = self.init_db()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO posts (
            author, html_content, publish_date, tags) VALUES (?,?,?,?)""",
            (post.author, post.html_content, post.publish_date, post.tags))
        conn.commit()
        conn.close()

    def get_recent_posts(self) -> list[object]:
        conn = self.init_db()
        cursor = conn.cursor()
        posts = []
        cursor.execute("""SELECT * FROM posts ORDER BY publish_date DESC LIMIT 5""")

        post_raw = cursor.fetchall()
        for p in post_raw:
            post = Post(p[0], p[1], p[2], p[3],p[4])
            posts.append(post)

        conn.close()
        return posts


db = Database()

for p in db.get_recent_posts():
    print(p.html_content, p.publish_date)