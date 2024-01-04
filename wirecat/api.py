import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from db import User, Post, UserMeta, PostMeta
from wirecat.util.w_secrets import Secrets

wc_api = Blueprint('api', __name__)

@wc_api.route('/api/v1')
def v1_help():
    #TODO
    #   return some json providing a top level overview of the api and how to use it
        return render_template('api-help.html')

@wc_api.route('/api/v1/posts')
def posts():
    #TODO:
    #   return json explaining how to auth and which child routes are available
    return ('post-help.html'), 200
@wc_api.route('/api/v1/posts/add', methods=['GET','POST'])
def add_post():
    if request.method == 'GET':
        return render_template(api-help.html), 200
    if request.method == 'POST':
        #TODO
        #   submit json containing api key and content
        #   verify request
        #   push to database
        #   update posts if published
        return render_template('api_request_success.html'), 200

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
