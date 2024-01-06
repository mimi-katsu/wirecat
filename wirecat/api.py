import os
import random
import string
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from bs4 import BeautifulSoup
from db import User, Post, PostMeta
from wirecat.util.catlib import catlib
from wirecat.app import db

wc_api = Blueprint('api', __name__)

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
        return redirect(url_for('wirecat.login')), 200
    if request.method == 'POST':
        key = request.form.get('key')
        api_user = request.form.get('username')
        user = User.query.filter_by(username=api_user).first()
        if user is None:
            return jsonify(error='Invalid Login')
        valid = check_password_hash(user.api_key, key)
        if valid:
            # initialize some useful values
            now = datetime.now()
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
            # Save the included files in a directory sturcture based on the date (YYYY/MM/DD)
            for f in request.files:
                file = request.files[f'{f}']
                if file and catlib.verify_post(request):
                    filename = secure_filename(file.filename)
                    path = catlib.make_current_dir_posts()
                    file.save(f'{path}/{filename}')
                else:
                    return jsonify(upload_type='post', success=False, msg='There was a problem uploading your post')
            return jsonify(upload_type='post', success=True, msg='Post was successfully uploaded'), 200
        else:
            return jsonify(error='Invalid Login')
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
