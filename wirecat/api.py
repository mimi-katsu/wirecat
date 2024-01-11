import os
import random
import string
import json
from datetime import datetime
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from db import User, Post, PostMeta, UserMeta, ApiKeys, Profile
from wirecat.util.catlib import catlib
from wirecat.app import db

wc_api = Blueprint('api', __name__)

class InvalidPost(Exception):
    def __str__(self):
        return "Post Failed Validation."

class InvalidCredentials(Exception):
    def __str__(self):
        return "Invalid Login"

class DoesNotExist(Exception):
    def __str__(self):
        return f'This object does not exist'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt','png', 'jpg', 'jpeg', 'gif', 'md'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@wc_api.route('/api/v1')
def v1_help():
    #TODO
    #   return some json providing a top level overview of the api and how to use it
        return render_template('api-help.html')

@wc_api.route('/api/v1/posts/get')
def get_posts():
    posts = Post.query.all()
    for p in posts:
        print(p.title, p.summary, p.author)
    #TODO:
    #   return json explaining how to auth and which child routes are available
    return redirect(url_for('wirecat.home')), 200

@wc_api.route('/api/v1/posts/add', methods=['GET','POST'])
def add_post():
    if request.method == 'GET':
        return jsonify(error="Invalid method"), 200

    if request.method == 'POST':
        try:
            response = None
            key = request.form.get('key', None)
            api_user = request.form.get('username', None)
            if not api_user and key:
                raise InvalidCredentials

            if key and api_user:
                user = User.query.options(joinedload(User.keys), joinedload(User.profile)).filter_by(username=api_user).first()
                print(user.id, user.keys.key, user.profile.dob, user.perm)
                # user_key = ApiKeys.query.filter_by(user_id = user.id).first()
                print("User: ",user.username, user.keys.key)
            if not user and user.keys.key:
                raise InvalidCredentials
            # match password hashes
            valid = check_password_hash(user.keys.key, key)
            print(valid)
            if not valid:
                raise InvalidCredentials

            if valid:
                # initialize some useful values
                now = datetime.now()
                # generate the realative path for the image 'src' attributes to use
                path = catlib.html_image_path()

                # create url slug from title
                slug = catlib.generate_slug(request.form.get('title', None))

                # TODO:
                # Incorporate post ids with post files so that same named files wont overwrite eachother when uploaded
                post_id = catlib.generate_id()
                print(post_id)
                # validate and post contents. returns true if okay. Raise error if bad
                if not catlib.verify_post(request):
                    raise InvalidPost

                # Save the included files in a directory structure based on the date (YYYY/MM/DD)
                for f in request.files:
                    file = request.files[f]
                    if file:
                        filename = secure_filename(file.filename)
                        print(filename)
                        #file save path is the absolute path for the file on the server
                        file.save(f'{catlib.file_save_path()}/{post_id}-{filename}')
                        print(f'{catlib.file_save_path()}/{post_id}-{filename}')
                # modify the image paths of the included html content and thumbnail to use the servers directory structure
                content_soup = BeautifulSoup(request.form.get('html_content', None), 'html.parser')

                images = content_soup.find_all('img')
                print(images)
                # replace image source with the relative path of the image file in servers storage
                for i in images:
                    i['src'] = f'{path}/{post_id}-{i["src"]}'
                    print(i)
                modified_html_content = str(content_soup)
                # Create SQLAlchemy object and push it to the database

                post = Post(
                    title=request.form.get('title', None),
                    user_id = user.id,
                    post_id = post_id,
                    slug=slug,
                    html_content=modified_html_content,
                    summary=request.form.get('summary', None),
                    publish_date=f'{now.year}/{now.month}/{now.day}'
                    )
                
                print('123')
                if request.form.get('thumbnail', None):
                    post.thumbnail = f'{post_id}-{request.form.get("thumbnail")}'
                print('thumb: ',post.thumbnail)    
                db.session.add(post)
                db.session.commit()
                #TODO:
                # Make sure that post files and database contents are both 
                # removed in the event that one or the other fails
            
                response = jsonify(type='post', success=True, msg='Post was successfully uploaded'), 200
            else:
                response = jsonify(type='post', success=False, msg='Post was invalidated')
        except IntegrityError as e:
            response = jsonify(type='post', success=False, msg=f'{str(e.orig)}'), 200
        
        except InvalidPost as e:
            response = jsonify(type='post', success=False, msg=f'{e}'), 200
        
        except InvalidCredentials as e:
            response = jsonify(type='post', success=False, msg=f'{e}'), 200

        finally:
            if not response:
                response = jsonify(error='Something Unexpected occured')
            return response

@wc_api.route('/api/v1/posts/delete/<post_id>', methods=['GET','POST'])
def delete(post_id):
    if request.method == 'GET':
        return jsonify(error="Invalid method"), 200

    if request.method == 'POST':
        try:
            response = None
            key = request.form.get('key', None)
            api_user = request.form.get('username', None)
            
            if not api_user and key:
                raise InvalidCredentials

            if key and api_user:
                user = User.query.filter_by(username=api_user).first()

            if not user and user.api_key:
                raise InvalidCredentials
            # match password hashes
            valid = check_password_hash(user.api_key, key)

            if not valid:
                raise InvalidCredentials

            if valid:
                post = Post.query.get(post_id)
                # if not post:
                #     raise DoesNotExist
                db.session.delete(post)
                db.session.commit()

                response = jsonify(type='delete', success=True, msg='Post was successfully deleted'), 200

        except InvalidCredentials as e:
            response = jsonify(type='delete', success=False, msg=f'{e}'), 200

        except DoesNotExist as e:
            repsonse = jsonify(type='delete', success=False, msg=f'{e}'), 200
        finally:
            if not response:
                response = jsonify(error="Something unexpected happened")
            return response

@wc_api.route('/api/v1/posts/unpublish')

@wc_api.route('/api/v1/posts/edit')

@wc_api.route('/api/v1/posts/update')
def update_posts():
    """Update posts held in memory. This will initiate the pulling of content from the 
    data base and refreshing of the content lists that are held in memory"""
    if request.headers.get('auth') != s.get_author_key():
        return 'Forbidden', 403
    else:
        # wirecat.posts.update(wirecat.db.get_recent_posts())
        return 'posts updated', 200

@wc_api.route('/api/v1/posts/highlight/<post_slug>')
def add_to_featured(post_slug):
    try:
        response = None
        key = request.form.get('key', None)
        api_user = request.form.get('username', None)
        
        if not api_user and key:
            raise InvalidCredentials

        if key and api_user:
            user = User.query.options(joinedload(User.keys)).filter_by(username=api_user).first()
            if user.perm != 'superadmin':
                raise InvalidCredentials
        if not user and user.api_key:
            raise InvalidCredentials
        # match password hashes
        valid = check_password_hash(user.keys.key, key)

        if not valid:
            raise InvalidCredentials
        
        if valid:
            post = Post.query.filter_by(slug=post_slug).first()
            if not post:
                raise DoesNotExist
            
            post.featured = True
            print(post.featured)
            db.session.commit()

            response = jsonify(type='feature', success=True, msg='Post was successfully featured'), 200

    except InvalidCredentials as e:
        response = jsonify(type='feature', success=False, msg=f'{e}'), 200

    except DoesNotExist as e:
        repsonse = jsonify(type='feature', success=False, msg=f'{e}'), 200
    finally:
        if not response:
            response = jsonify(error="Something unexpected happened")
        return response
    
@wc_api.route('/api/v1/posts/highlight/add')

@wc_api.route('/api/v1/posts/highlight/remove')
def remove_post():
    return
