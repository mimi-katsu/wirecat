from datetime import datetime
import random
import string

class Post:
    def __init__(self, post_id=None, title=None, author=None, html_content=None, summary=None, thumbnail=None, publish_date=None, tags=None):
        self.id = post_id
        self.title = title
        self.author:str = author
        self.html_content:str = html_content
        self.summary = summary
        if not thumbnail:
            self.thumbnail = "static/images/default-thumb.png"
        else:
            self.thumbnail = thumbnail
        self.publish_date:str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.tags = tags
        self.generate_id()

    def generate_id(self, length=5):
        '''create an alphanumeric post id if it doesn't exist already'''
        if not self.id:
            characters = string.ascii_letters + string.digits 
            random_id = ''.join(random.choice(characters) for _ in range(length))
            self.id = f'post-{random_id}'

class Posts:
    posts = {}
    def __init__(self):
        self.posts:dict = {}

    def get_post(self, post_id):
        if post_id in self.posts.keys():
            p = self.posts[post_id]
            return p

    def get_popular(self, posts):
        """sort list of posts by popularity"""
        return
    def get_latest(self, posts):
        """sort list of postsfrom newest to oldest"""
        return

    def get_featured(self, posts:list[object]) -> list[object]:
        """get posts specified in featured list for special placement within home page"""
        return

    def update(self, posts):
        for p in posts:
            self.posts[p.id] = p
        