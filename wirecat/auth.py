import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

wc_auth = Blueprint('wc_auth_auth', __name__, url_prefix='/auth')

@wc_auth.route('/login', methods=['GET', 'POST'])
def login_api():
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/forum')

@wc_auth.route('/logout')

@wc_auth.route('/verify', methods = ['GET', 'POST'])
def verify():
    """verify requests made to the api with an api key or HMAC authentication"""
    if request.method == 'GET':
        return jsonify(verified=False)
    
    if request.method == 'post' and request.headers.get('auth'):
        key = request.headers.get('auth')
        state = s.verify_key(key)
        return jsonify(verified=state)

    #TODO
    #Verify requests that use HMAC and not an api key
    return 'Success', 200