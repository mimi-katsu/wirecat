"""
All sections of this page are tagged with the following titles in order to be easily 
searchable. MAIN~,API/AUTH~, etc.

Sections:
    MAIN~
    API~
        API/AUTH~
    ERRORS~

    love, 
        mimi
"""
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from db import User, Post, PostMeta
from wirecat.util.w_secrets import Secrets
s = Secrets()

wc = Blueprint('wirecat', __name__)
#-------------------------------------------------------------------------------------------------#
#   MAIN~ - Routes for main pages
#-------------------------------------------------------------------------------------------------#

@wc.route('/home')
@wc.route('/index')
@wc.route('/')
def home():
    post_id = 1
    best = Post.query.all()
    for b in best:
        if not b.thumbnail:
            b.thumbnail = '/static/images/default-thumb.png'
    return render_template('frontpage.html', best_posts=[best[0]])
    # return render_template('frontpage.html')
@wc.route('/downloads')
def downloads():
    return render_template('downloads.html')

@wc.route('/forum')
def community():
    return render_template('forum.html')

@wc.route('/blog')
def blog():
    return 'Blog'

@wc.route('/blog/<post_id>')
def blog_post(post_id):
    p = Post.query.get(post_id)
    return render_template('post.html', post=p)

@wc.route('/login')
def login():
    return render_template('login.html')
