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
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from db import User, Post, PostMeta, UserMeta, ApiKeys, Profile
from wirecat.util.w_secrets import Secrets
from wirecat.app import db

s = Secrets()

wc = Blueprint('wirecat', __name__)
#-------------------------------------------------------------------------------------------------#
#   MAIN~ - Routes for main pages
#-------------------------------------------------------------------------------------------------#

@wc.route('/home')
@wc.route('/index')
@wc.route('/')
def home():
    # try:
    #     verify_jwt_in_request(optional=True)
    #     current_user = get_jwt_identity()
    #     is_logged_in = True
    # except NoAuthorizationError:
    #     current_user = None
    #     is_logged_in = False
    best = Post.query.all()
    for b in best:
        if not b.thumbnail:
            b.thumbnail = '/static/images/default-thumb.png'
    return render_template('frontpage.html', best_posts=[best[0]], all_posts = best)

    # return render_template('frontpage.html')

@wc.route('/profiles/<user_slug>')
def profile(user_slug):
    db_user = User.query.options(joinedload(User.meta), joinedload(User.profile)).filter_by(username=user_slug).first()
    posts = Post.query.filter_by(user_id = db_user.id).all()
    return render_template('profile.html', user=db_user, posts=posts)

@wc.route('/dashboard')
@jwt_required()
def dashboard():
    user = get_jwt_identity()
    if not user:
        return redirect(url_for('wirecat.login'))

    db_user = User.query.options(joinedload(User.meta), joinedload(User.profile)).filter_by(username=user).first()
    return render_template('dashboard.html', user=db_user)
    
@wc.route('/downloads')
def downloads():
    return render_template('downloads.html')

@wc.route('/forum')
def community():
    return render_template('forum.html')

@wc.route('/p')
def blog():
    return 'Blog'

@wc.route('/post/<post_slug>')
def blog_post(post_slug):
    post = get_post(post_slug)
    return render_template('post.html', post=post)

@wc.route('/login')
def login():
    return render_template('login.html')

def get_post(url_slug):
    p = Post.query.options(joinedload(Post.author)).filter_by(slug=url_slug).first()
    if not p.meta:
        meta = PostMeta(post_id=p.id)
        db.session.add(meta)
        db.session.commit()
    p.meta.views += 1
    db.session.commit()
    return p

@wc.context_processor
def check_login():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    login_status = {'logged_in': False}
    if current_user:
        login_status=  {'logged_in':True}
    return login_status
    # try:
    #     verify_jwt_in_request(optional=True)
    #     current_user = get_jwt_identity()
    #     print(current_user)
    #     login_status=  {'logged_in':True}
    # except NoAuthorizationError:
    #     current_user = None
    #     login_status = {'logged_in': False}

    # finally:
        # return login_status