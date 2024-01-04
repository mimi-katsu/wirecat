import functools
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

wc_auth = Blueprint('wc_auth_auth', __name__, url_prefix='/auth')

@wc_auth.route('/login', methods=['GET', 'POST'])
def login_api():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        print(request.data)
        username = request.form.get('username', None)

        password = request.form.get('password', None)
        print(username, password)
        #TODO
        # query  db with username to get pass hash
        # hash provided pass and compare to stored hash
        # if hashes match create token
        expiry = datetime.timedelta(days=1)
        token = create_access_token(identity=username, expires_delta=expiry)
        response = jsonify(logged_in=True)
        set_access_cookies(response, token)
        return response

@wc_auth.route('/logout')

@wc_auth.route('/verify', methods = ['GET', 'POST'])
@jwt_required()
def verify():
    """verify requests made to the api with an api key or HMAC authentication"""
    # if request.method == 'GET':
    #     return render_template('login')
    
    # if request.method == 'POST': 
    token = request.cookies.get('access_token_cookie')
    if not token:
        return render_template('login.html')
    current_user = get_jwt_identity()
    return jsonify(logged_in=True)
    #TODO
    #Verify requests that use HMAC and not an api key
    # return 'Success', 200