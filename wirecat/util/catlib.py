import sqlite3
import os
from datetime import datetime
import random
import string
import secrets
import re
from db import Post
class catlib:

        def generate_api_key():
                return secrets.token_hex(32)

        def generate_id(length=24):
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

        def generate_slug(title):
                # Convert to lowercase
                slug = title.lower()
                # Replace spaces and underscores with hyphens
                slug = re.sub(r'[\s_]+', '-', slug)
                # Remove all characters that are not alphanumerics or hyphens
                slug = re.sub(r'[^\w-]', '', slug)
                # Remove leading, trailing, or multiple consecutive hyphens
                slug = re.sub(r'-+', '-', slug).strip('-')
                return slug
        
        def serialize_posts(orm_obj_list):
                posts = []
                for obj in orm_obj_list:
                        post = {}
                        post['id'] = obj.id
                        post['post_id']=obj.post_id
                        post['slug']=obj.slug
                        post['title']=obj.title
                        post['summary']=obj.summary
                        post['thumbnail']=obj.thumbnail
                        post['publish_date']=obj.publish_date
                        posts.append(post)
                return posts

        def serialize_posts_for_admin(orm_obj_list):
                posts = []
                for obj in orm_obj_list:
                        post = {}
                        post['id'] = obj.id
                        post['post_id']=obj.post_id
                        post['slug']=obj.slug
                        post['title']=obj.title
                        post['publish_date']=obj.publish_date
                        post['author'] = obj.author.username
                        posts.append(post)
                return posts

        def deserialize_posts(serialized_obj_list):
                posts = []
                for obj in serialized_obj_list:
                        post = Post(id=obj['id'], post_id=obj['post_id'],slug=obj['slug'], title=obj['title'], summary=obj['summary'], thumbnail=obj['thumbnail'], publish_date=obj['publish_date'])
                        posts.append(post)
                return posts