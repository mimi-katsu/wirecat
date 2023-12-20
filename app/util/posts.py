from datetime import datetime

class Post:
    def __init__(self, id_num=None, author=None, html_content=None, publish_date=None, tags=None):
        self.id = id_num
        self.author:str = author
        self.html_content:str = html_content
        self.publish_date:str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.tags = tags

class Posts:
    def get_popular(self, posts):
        """sort list of posts by popularity"""
        return
    def get_latest(self, posts):
        """sort list of postsfrom newest to oldest"""
        return

    def get_featured(self, posts:list[object]) -> list[object]:
        """get posts specified in featured list for special placement within home page"""
        return