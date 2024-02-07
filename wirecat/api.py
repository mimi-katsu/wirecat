import os
import random
import string
import json
from datetime import datetime
import secrets
from bs4 import BeautifulSoup

from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint, current_app

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from wirecat.db import User, Post, PostMeta, UserMeta, ApiKeys, Profile, Announcement
from wirecat.util.catlib import catlib
from wirecat.app import db

wc_api = Blueprint('api', __name__)

can_post = ['superadmin', 'admin', 'author']
see_own_stats = ['superadmin', 'admin', 'author']
see_all_stats = ['superadmin', 'admin']
can_create_post= ['superadmin', 'admin', 'author']
can_publish = ['admin', 'superadmin', 'admin']
can_delete = ['admin', 'superadmin']
can_highlight = ['admin', 'superadmin']
can_register_users = ['admin', 'superadmin']
can_register_admins = ['superadmin']
autogen_api_key_users = ['superadmin', 'admin', 'author']
make_announcement_users = ['superadmin', 'admin']


id_types = {'username', 'id', 'url_slug'}
user_attr = {'first_name', 'last_name', 'gender', 'photo_path', 'signature', 'experience', 'about'}

def get_verify_api_user(request):
    key = request.form.get('key', None)
    api_user = request.form.get('username', None)
    if not api_user and key:
        raise InvalidCredentials

    user = User.query.options(joinedload(User.keys)).filter_by(username=api_user).first()
    if not user:
        raise InvalidCredentials
    # check for api key
    if not user.keys.key:
        raise InvalidCredentials
    # match password hashes
    valid = check_password_hash(user.keys.key, key)
    if not valid:
        raise InvalidCredentials    

    return user

class InvalidRequest(Exception):
    def __str__(self):
        return "Request Failed Validation. Please ensure all necessary parameters are provided"

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

@wc_api.route('/api/v1/posts/get/hidden', methods=['GET'])
def get_hidden():
    try:
        response = None
        # verify credentials in request and return the associated user if valid. 
        user = get_verify_api_user(request)
        
        if user.perm not in current_app.config['CAN_PUBLISH']:
            raise InvalidCredentials

        posts = Post.query.options(joinedload(Post.author)).filter_by(published=False).all()

        if not posts:
            raise DoesNotExist

        post_json = catlib.serialize_posts_for_admin(posts)

        response = jsonify(type='get', success=True, msg=post_json, usr=user.username), 200

    except InvalidCredentials as e:
        db.session.rollback()
        response = jsonify(type='get', success=False, msg=f'{e}'), 403
    except Exception as e:
        db.session.rollback()
        response = jsonify(type='get', success=False, msg=f'{e}'), 500
    except DoesNotExist as e:
        db.session.rollback()
        response = jsonify(type='get', success=False, msg=f'{e}'), 404
    finally:
        if not response:
            response = jsonify(error="Something unexpected happened"), 500
        return response


@wc_api.route('/api/v1/posts/add', methods=['GET','POST'])
def add_post():
    if request.method == 'GET':
        return jsonify(error="Invalid method"), 200

    if request.method == 'POST':
        try:
            response = None

            user = get_verify_api_user(request)

            if user.perm not in current_app.config["CAN_POST"]:
                raise InvalidCredentials

            # initialize some useful values
            now = datetime.now()

            # generate the relative path for the image 'src' attributes to use
            path = catlib.html_image_path()

            # create url slug from title
            slug = catlib.generate_slug(request.form.get('title', None))

            post_id = catlib.generate_id()

            # validate and post contents. returns true if okay. Raise error if bad
            # TODO:
            # This function doesn nothing at the moment. In the future it should sanitize the
            # post contents and verify the necessary fileds exist
            if not catlib.verify_post(request):
                raise InvalidRequest

            # Save the included files in a directory structure based on the date (YYYY/MM/DD)
            for f in request.files:
                file = request.files[f]
                if file:
                    filename = secure_filename(file.filename)
                    #file save path is the absolute path for the file on the server
                    file.save(f'{catlib.file_save_path()}/{post_id}-{filename}')

            # modify the image paths of the included html content and thumbnail to use the servers directory structure
            content_soup = BeautifulSoup(request.form.get('html_content', None), 'html.parser')
            images = content_soup.find_all('img')
            # replace image source with the relative path of the image file in servers storage
            for i in images:
                i['src'] = f'{path}/{post_id}-{i["src"]}'
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
            
            if request.form.get('thumbnail', None):
                post.thumbnail = f'{post_id}-{request.form.get("thumbnail")}'
            
            db.session.add(post)
            db.session.commit()
            #TODO:
            # Make sure that post files and database contents are both 
            # removed in the event that one or the other fails


            # Update latest post cache
            cache = current_app.cache
            latest = Post.query.order_by(Post.publish_date.desc()).limit(5)
            to_cache = catlib.serialize_posts(latest)
            cache.set('latest', to_cache)

            response = jsonify(type='post', success=True, msg='Post was successfully uploaded'), 200

        except IntegrityError as e:
            response = jsonify(type='post', success=False, msg=f'{str(e.orig)}'), 200
        
        except InvalidRequest as e:
            response = jsonify(type='post', success=False, msg=f'{e}'), 200
        
        except InvalidCredentials as e:
            response = jsonify(type='post', success=False, msg=f'{e}'), 200
        except Exception as e:
            response = jsonify(type='feature', success=False, msg=f'{e}'), 200
        finally:
            if not response:
                response = jsonify(error='Something Unexpected occured')
            return response

@wc_api.route('/api/v1/posts/delete/<id_type>/<target>', methods=['GET','DELETE'])
def delete_post(id_type, target):
    if request.method != 'DELETE':
        return jsonify(type='delete', success=False, msg='Invalid Method'), 200
    try:
        response = None
        user = get_verify_api_user(request)

        if user.perm not in current_app.config["CAN_DELETE"]:
            raise InvalidCredentials

        if id_type == 'slug':
            post = Post.query.filter_by(slug=target).first()
        if id_type == 'id':
            post = Post.query.filter_by(id=target).first()

        if not post:
            raise DoesNotExist

        current_app.cache.set('best', "")
        current_app.cache.set('featured', "")
        current_app.cache.set('latest', "")

        meta = PostMeta.query.filter_by(post_id=post.id).first()
        if meta:
            db.session.delete(meta)
        db.session.delete(post)
        db.session.commit()

        response = jsonify(type='delete', success=True, msg='Post was successfully deleted'), 200

    except InvalidCredentials as e:
        response = jsonify(type='delete', success=False, msg=f'{e}'), 200

    except DoesNotExist as e:
        response = jsonify(type='delete', success=False, msg=f'{e}'), 200
        
    except Exception as e:
        response = jsonify(type='delete', success=False, msg=f'{e}'), 200
    finally:
        if not response:
            response = jsonify(error="Something unexpected happened")
        return response

@wc_api.route('/api/v1/posts/publish/<id_type>/<target>',methods=['GET','POST'])
def publish(id_type, target):
    try:
        response = None
        user = get_verify_api_user(request)
        
        if user.perm not in current_app.config["CAN_PUBLISH"]:
            raise InvalidCredentials

        if id_type == 'slug':
            post = Post.query.filter_by(slug=target).first()
        if id_type == 'id':
            post = Post.query.filter_by(id=target).first()

        if not post:
            raise DoesNotExist

        post.published = True
        db.session.commit()

        response = jsonify(type='publish', success=True, msg='Post was successfully published'), 200

    except InvalidCredentials as e:
        db.session.rollback()
        response = jsonify(type='publish', success=False, msg=f'{e}'), 200
    except Exception as e:
        db.session.rollback()
        response = jsonify(type='publish', success=False, msg=f'{e}'), 200
    except DoesNotExist as e:
        db.session.rollback()
        response = jsonify(type='publish', success=False, msg=f'{e}'), 200
    finally:
        if not response:
            response = jsonify(error="Something unexpected happened")
        return response

@wc_api.route('/api/v1/posts/hide/<id_type>/<target>',methods=['GET','POST'])
def hide(id_type, target):
    try:
        response = None
        user = get_verify_api_user(request)
        
        if user.perm not in current_app.config["CAN_PUBLISH"]:
            raise InvalidCredentials

        if id_type == 'slug':
            post = Post.query.filter_by(slug=target).first()
        if id_type == 'id':
            post = Post.query.filter_by(id=target).first()

        if not post:
            raise DoesNotExist

        post.published = False
        db.session.commit()

        response = jsonify(type='hide', success=True, msg='Post was successfully hidden'), 200

    except InvalidCredentials as e:
        db.session.rollback()
        response = jsonify(type='hide', success=False, msg=f'{e}'), 200
    except Exception as e:
        db.session.rollback()
        response = jsonify(type='hide', success=False, msg=f'{e}'), 200
    except DoesNotExist as e:
        db.session.rollback()
        response = jsonify(type='hide', success=False, msg=f'{e}'), 200
    finally:
        if not response:
            response = jsonify(error="Something unexpected happened")
        return response

@wc_api.route('/api/v1/posts/highlight/add/<id_type>/<target>')
def highlight(id_type, target):
    try:
        response = None
        user = get_verify_api_user(request)
        
        if user.perm not in can_highlight:
            raise InvalidCredentials

        if id_type == 'slug':
            post = Post.query.filter_by(slug=target).first()
        if id_type == 'id':
            post = Post.query.filter_by(id=target).first()

        if not post:
            raise DoesNotExist

        post.featured = True
        db.session.commit()

        # Update featured post cache
        cache = current_app.cache
        featured = Post.query.filter_by(featured=True).limit(5)
        to_cache = catlib.serialize_posts(featured)
        cache.set('featured', to_cache)

        response = jsonify(type='feature', success=True, msg='Post was successfully featured'), 200

    except InvalidCredentials as e:
        response = jsonify(type='feature', success=False, msg=f'{e}'), 200
    except Exception as e:
        response = jsonify(type='feature', success=False, msg=f'{e}'), 200
    except DoesNotExist as e:
        response = jsonify(type='feature', success=False, msg=f'{e}'), 200
    finally:
        if not response:
            response = jsonify(error="Something unexpected happened")
        return response
  
@wc_api.route('/api/v1/posts/highlight/remove/<id_type>/<target>')
def unhighlight(id_type, target):
    try:
        response = None
        user = get_verify_api_user(request)
        
        if user.perm not in current_app.config["CAN_HIGHLIGHT"]:
            raise InvalidCredentials

        if not user.keys.key:
            raise InvalidCredentials
        # match password hashes
        valid = check_password_hash(user.keys.key, key)
        if not valid:
            raise InvalidCredentials

        if id_type == 'slug':
            post = Post.query.filter_by(slug=target).first()
        if id_type == 'id':
            post = Post.query.filter_by(id=target).first()

        if not post:
            raise DoesNotExist

        post.featured = False
        db.session.commit()

        # Update featured post cache
        cache = current_app.cache
        featured = Post.query.filter_by(featured=True).limit(5)
        to_cache = catlib.serialize_posts(featured)
        cache.set('featured', to_cache)

        response = jsonify(type='unfeature', success=True, msg='Post was successfully removed from featured list'), 200

    except InvalidCredentials as e:
        response = jsonify(type='feature', success=False, msg=f'{e}'), 200
    except Exception as e:
        response = jsonify(type='feature', success=False, msg=f'{e}'), 200
    except DoesNotExist as e:
        response = jsonify(type='feature', success=False, msg=f'{e}'), 200
    finally:
        if not response:
            response = jsonify(error="Something unexpected happened")
        return response

@wc_api.route('/api/v1/users/register')
def register_user():
    try:
        response = None
        user = get_verify_api_user(request)

        new_user = request.form.get('newuser', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        access_level = request.form.get('access_level', None)


        if not new_user or not email or not password:
            raise InvalidRequest

        hashed_pass = generate_password_hash(password, method='pbkdf2:sha256')
        
        if user.perm not in current_app.config["CAN_REGISTER_USERS"]:
            raise InvalidCredentials

        date = datetime.now()
        newuser = User(username = new_user, email = email, password = hashed_pass, creation_date=f'{date.year}/{date.month}/{date.day}' )
        
        if access_level:
            newuser.perm = access_level
        # add user 

        db.session.add(newuser)
        db.session.commit()

        # add user Profile, Meta and Keys if needed
        newuser = User.query.filter_by(username = newuser.username).first()
        newuser_profile = Profile(user_id = newuser.id)
        newuser_meta = UserMeta(user_id = newuser.id)
        if newuser.perm in autogen_api_key_users:
            key = secrets.token_hex(32)
            hashed_key = generate_password_hash(key, method='pbkdf2:sha256')
            user_key = ApiKeys(user_id=user.id, key = hashed_key, expires='never')
            db.session.add(user_key)
            db.session.commit()
        db.session.add(newuser_profile)
        db.session.add(newuser_meta)
        db.session.commit()
        response = jsonify(type='get', success=True, msg=f"User {newuser} was successfully created"), 200

    except IntegrityError as e:
        db.session.rollback()
        response = jsonify(type='register', success=False, msg=f'{str(e.orig)}'), 200

    except InvalidRequest as e:
        response = jsonify(type='register', success=False, msg=f'{str(e)}'), 200

    except InvalidCredentials as e:
        db.session.rollback()
        response = jsonify(type='register', success=False, msg=f'{e}'), 200

    except Exception as e:
        db.session.rollback()
        response = jsonify(type='register', success=False, msg=f'{e}'), 200

    finally:
        if not response:
            response = jsonify(error="Something unexpected happened")
        return response

@wc_api.route('/api/v1/announcements/add', methods=['POST'])
def make_announcement():
    try:
        response = None
        user = get_verify_api_user(request)
        ann = request.form.get('announcement', None)

        if not ann:
            raise InvalidRequest
        
        if user.perm not in current_app.config["CAN_MAKE_ANNOUNCEMENTS"]:
            raise InvalidCredentials

        date = datetime.now()

        announcement = Announcement(author = user.username, content = ann, post_date=f'{date}' )


        db.session.add(announcement)
        db.session.commit()

        current_app.cache.set('announcement', ann)
        print(ann)
        response = jsonify(type='Announce', success=True, msg=f"Announcement was successfully created"), 200

    except IntegrityError as e:
        db.session.rollback()
        response = jsonify(type='Announce', success=False, msg=f'{str(e.orig)}'), 200

    except InvalidRequest as e:
        response = jsonify(type='Announce', success=False, msg=f'{str(e)}'), 200

    except InvalidCredentials as e:
        db.session.rollback()
        response = jsonify(type='Announce', success=False, msg=f'{e}'), 200

    except Exception as e:
        db.session.rollback()
        response = jsonify(type='Announce', success=False, msg=f'{e}'), 200

    finally:
        if not response:
            response = jsonify(error="Something unexpected happened")
        return response

# @wc_api.route('/api/v1/users/update/<id_type>/<target>/<param>')
# def update_user(id_type,target,param,value):

    
#     try:
#         response = None

#         if id_type not in id_types:
#             raise InvalidRequest

#         if param not in user_attr:
#             raise InvalidRequest

#         key = request.form.get('key', None)
#         api_user = request.form.get('username', None)

#         if not api_user and key:
#             raise InvalidCredentials

#         if key and api_user:
#             user = User.query.options(joinedload(User.keys)).filter_by(username=api_user).first()

#         if not user.keys.key:
#             raise InvalidCredentials
#         # match password hashes
#         valid = check_password_hash(user.keys.key, key)
#         if not valid:
#             raise InvalidCredentials

#         if id_type == 'id':
#             profile = Profile.query.filter_by(user_id=target).first()
#         if id_type == 'username':
#             user = Profile.query.filter_by(user_id=target).first()

#         if not user:
#             raise DoesNotExist

        

#         db.session.commit()

#         response = jsonify(type='Update User', success=True, msg='User was successfully updated'), 200
#     except InvalidRequest as e:
#         response = jsonify("Type":"Update User", "Status": "Failed", "Msg":f"{e}")
#     except InvalidCredentials as e:
#         response = jsonify(type='feature', success=False, msg=f'{e}'), 200
#     except Exception as e:
#         response = jsonify(type='feature', success=False, msg=f'{e}'), 200
#     except DoesNotExist as e:
#         response = jsonify(type='feature', success=False, msg=f'{e}'), 200
#     finally:
#         if not response:
#             response = jsonify(error="Something unexpected happened")
#         return response