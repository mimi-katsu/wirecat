class User:
    def __init__(self, uid=None, username=None, first_name=None, last_name=None, email=None, date_created=None, favorites=[]):
        self.uid:str = uid
        self.username:str = username
        self.first_name:str = first_name
        self.last_name:str = last_name
        self.email:str = email
        self.date_created:str = date_created
        self.favorites:list[str] = favorites

    def favorites(self):
        """return a list of posts that the user has "favorited" on the blog"""
        return
    def comments(self):
        """return list of comments that the user has left on blog posts"""
        return
    def view_history(self):
        """return a list of pages visited in chronological order (reverse)"""
        return