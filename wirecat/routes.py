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
from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint, abort, current_app, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, jwt_required, get_jwt, unset_jwt_cookies
from flask_jwt_extended.exceptions import NoAuthorizationError
from sqlalchemy.orm import joinedload
from db import User, Post, PostMeta, UserMeta, ApiKeys, Profile, Announcement
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

    ann = cache.get('anonouncement')
    if not ann:
        ann = Announcement.query.order_by(Announcement.post_date.desc()) \
        .limit(1).first()
        print(ann.content)
        cache.set('announcement', ann.content)

    if not featured:
        current_app.logger.info('DBQUERY: Featured Posts: CACHE')
        featured = Post.query.filter_by(featured=True, published=True) \
        .all()
        to_cache = catlib.serialize_posts(featured)
        cache.set('featured', to_cache)

    if not latest:
        latest = Post.query.order_by(Post.publish_date.desc()) \
        .filter_by(published=True) \
        .limit(5) \
        .all()
        
        to_cache = catlib.serialize_posts(latest)
        cache.set('latest', to_cache)

    if not best:
        best = Post.query.join(PostMeta) \
        .order_by(PostMeta.views.desc()) \
        .limit(5) \
        .all()
        
        to_cache = catlib.serialize_posts(best)
        cache.set('best', to_cache)

    for b in featured:
        if not b.thumbnail:
            b.thumbnail = '/static/images/default-thumb.png'
    return render_template('frontpage.html', featured=featured, latest_posts = latest, best_posts = best, announcement=ann.content)

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

    db_user = User.query.options(joinedload(User.meta), joinedload(User.profile), joinedload(User.keys)).filter_by(username=user).first()
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
    if not post:
        abort(404)
    return render_template('post.html', post=post)

@wc.route('/login')
def login():
    return render_template('login.html')

@wc.route('/logout', methods=['GET','POST'])
def logout():
    response = make_response(redirect(url_for('wirecat.home')))  # Redirect to home or login page
    unset_jwt_cookies(response)  # This will remove the JWT cookies
    return response

def get_post(url_slug):
    p = Post.query.options(joinedload(Post.author)).filter_by(slug=url_slug).first()
    if p:
        if not p.meta:
            meta = PostMeta(post_id=p.id)
            db.session.add(meta)
            db.session.commit()
        p.meta.views += 1
        db.session.commit()
        return p
    return None

@wc.context_processor
def check_login():
    verify_jwt_in_request(optional=True)
    token_values = get_jwt()
    login_status = {'logged_in': False}
    user = token_values.get('sub')
    if user:
        auth_level = token_values.get('auth_level')
        login_status=  {'logged_in':True, 'auth_level': auth_level}
    return login_status