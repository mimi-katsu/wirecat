class Post:
    def __init__(self):
        self.author:str = ""
        self.html_content:str = ""
        self.publish_date:int = None
        

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