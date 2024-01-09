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
from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint, abort
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
    return render_template('frontpage.html', best_posts=[best[0]], all_posts = best)
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

@wc.route('/blog/<url_slug>')
def blog_post(url_slug):
    p = Post.query.filter_by(slug=url_slug).first()
    return render_template('post.html', post=p)

@wc.route('/login')
def login():
    return render_template('login.html')
