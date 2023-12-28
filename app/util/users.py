import random
import string
from datetime import datetime
import random
import string
import hashlib
class Users:
    def generate_id(self, user:object, length=12):
        '''create an alphanumeric post id if it doesn't exist already'''
        characters = string.ascii_letters + string.digits 
        random_id = ''.join(random.choice(characters) for _ in range(length))
        user.id = f'user-{random_id}'
        

class User:
    def __init__(self, user_id=None, username=None, first_name=None, last_name=None, email=None, date_created=None, favorites=[], api_key=None, secret_key=None, password=None):
        self.user_id:str = user_id
        self.username:str = username
        self.first_name:str = first_name
        self.last_name:str = last_name
        self.email:str = email
        self.date_created:str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.favorites:list[str] = favorites
        self.api_key = api_key
        self.secret_key = secret_key
        self.password = password

    def favorites(self):
        """return a list of posts that the user has "favorited" on the blog"""
        return
    def comments(self):
        """return list of comments that the user has left on blog posts"""
        return
    def view_history(self):
        """return a list of pages visited in chronological order (reverse)"""
        return
