import functools
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, make_response
)
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from db import User
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

wc_auth = Blueprint('wc_auth_auth', __name__, url_prefix='/auth')

@wc_auth.route('/login', methods=['GET', 'POST'])
def login_api():
    if request.method == 'GET':
        return redirect(url_for('wirecat.login'))
    if request.method == 'POST':
        # get client credentials from http post form
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        req_type = request.form.get('request_type', None)
            
        # pull user information from database
        if username and password:
            user = User.query.filter_by(username=username).first()

            if user is None:
                # If user doesn't exist, redirect back to login and display invalid login message
                flash('Invalid login')
                return redirect('/login')
        else:
            return redirect(url_for('wirecat.login'))
        # hash provided password and compare
        recv_hash = generate_password_hash(password)
        valid = check_password_hash(generate_password_hash(user.password), password)

        if valid:
            # check for request_type filed in form. If it exists, a json response is built. If not, a redirection response to /home is built and the token
            # is set as a cookie. This is so that scripts that require json can interact with the api, but no unneccessary info is sent to a browser client
            if req_type == 'json':
                expiry = datetime.timedelta(minutes=1)
                token = create_access_token(identity=username, expires_delta=expiry)
                response = jsonify(logged_in=True, token=token)
                return response
            else:
                expiry = datetime.timedelta(hours=12)
                token = create_access_token(identity=username, expires_delta=expiry)
                response = make_response(redirect(url_for('wirecat.home')))
                set_access_cookies(response, token)
                return response
        else:
            # if credentials are invalid, redirect back to login and display invalid login message
            flash('Invalid login')
            return redirect('/login')

@wc_auth.route('/logout')

@wc_auth.route('/verify', methods = ['GET', 'POST'])
@jwt_required()
def verify():
    """verify requests made to the api with an api key or HMAC authentication"""
    token = request.cookies.get('access_token_cookie')
    if not token:
        return render_template('login.html')
    current_user = get_jwt_identity()
    return jsonify(logged_in=True, user = current_user)
    #TODO
    #Verify requests that use HMAC and not an api key
    # return 'Success', 200