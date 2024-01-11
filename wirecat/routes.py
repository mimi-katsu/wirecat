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
from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint, abort, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from db import User, Post, PostMeta, UserMeta, ApiKeys, Profile
from wirecat.util.w_secrets import Secrets
from wirecat.app import db
from wirecat.util.catlib import catlib
s = Secrets()

wc = Blueprint('wirecat', __name__)
#-------------------------------------------------------------------------------------------------#
#   MAIN~ - Routes for main pages
#-------------------------------------------------------------------------------------------------#

@wc.route('/home')
@wc.route('/index')
@wc.route('/')
def home():
    cache = current_app.cache

    featured = cache.get('featured')
    if featured:
        featured = catlib.deserialize_posts(featured)

    latest = cache.get('latest')
    if latest:
        latest = catlib.deserialize_posts(latest)

    best = cache.get('best')
    if best:
        best = catlib.deserialize_posts(best)

    if not featured:
        featured = Post.query.filter_by(featured=True).limit(5)
        to_cache = catlib.serialize_posts(featured)
        cache.set('featured', to_cache)

    if not latest:
        latest = Post.query.order_by(Post.publish_date).limit(5)
        to_cache = catlib.serialize_posts(latest)
        cache.set('latest', to_cache)

    if not best:
        best = Post.query.join(PostMeta).order_by(PostMeta.views.desc()).limit(5).all()
        to_cache = catlib.serialize_posts(best)
        cache.set('best', to_cache)

    for b in featured:
        if not b.thumbnail:
            b.thumbnail = '/static/images/default-thumb.png'
    return render_template('frontpage.html', featured=featured, latest_posts = latest, best_posts = best)

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