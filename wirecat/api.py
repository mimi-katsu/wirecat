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
from db import User, Post, PostMeta
from wirecat.util.catlib import catlib
from wirecat.app import db

wc_api = Blueprint('api', __name__)

class InvalidPost(Exception):
    def __str__(self):
        return "Post Failed Validation."

class InvalidCredentials(Exception):
    def __str__(self):
        return "Invalid Login"

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
                # initialize some useful values
                now = datetime.now()
                # TODO:
                # Incorporate post ids with post files so that same named files wont overwrite eachother when uploaded
                post_id = catlib.generate_id()
                # Create SQLAlchemy object and push it to the database
                post = Post(
                    title=request.form.get('title', None),
                    author=user.username,
                    html_content=request.form.get('html_content', None),
                    summary=request.form.get('summary', None),
                    thumbnail=request.form.get('thumbnail', None),
                    tags=request.form.get('tags', None),
                    publish_date=f'{now.year}/{now.month}/{now.day}'
                    )
                db.session.add(post)
                db.session.commit()
                #TODO:
                # Make sure that post files and database contents are both 
                # removed in the event that one or the other fails

                # validate and post contents. returns true if okay. Raise error if bad
                if not catlib.verify_post(request):
                    raise InvalidPost
                # Save the included files in a directory structure based on the date (YYYY/MM/DD)
                for f in request.files:
                    file = request.files[f]
                    if file:
                        filename = secure_filename(file.name)
                        # create the directory paths if needed and return the absolute path
                        path = catlib.make_current_dir_posts()
                        file.save(f'{path}/{filename}')
                
            response = jsonify(upload_type='post', success=True, msg='Post was successfully uploaded'), 200
        
        except IntegrityError as e:
            response = jsonify(upload_type='post', success=False, msg=f'{str(e.orig)}'), 200
        
        except InvalidPost as e:
            response = jsonify(upload_type='post', success=False, msg=f'{e}'), 200
        
        finally:
            return response

@wc_api.route('/api/v1/posts/delete', methods=['GET','POST'])
def delete():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

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

@wc_api.route('/api/v1/posts/highlight')

@wc_api.route('/api/v1/posts/highlight/add')

@wc_api.route('/api/v1/posts/highlight/remove')
def remove_post():
    return
