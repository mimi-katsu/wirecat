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
from flask import Flask, render_template, request, jsonify, redirect    
from wirecat.util.catlib import WireCat
from wirecat.util.w_secrets import Secrets
from wirecat import app

wirecat = WireCat()
wirecat.posts.update(wirecat.db.get_recent_posts())
s = Secrets()

#-------------------------------------------------------------------------------------------------#
#   MAIN~ - Routes for main pages
#-------------------------------------------------------------------------------------------------#

@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    best = wirecat.db.get_recent_posts()
    latest  = best[0]
    return render_template('frontpage.html', best_posts=[best[0]], latest_post=latest)

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/forum')
def community():
    return render_template('forum.html')

@app.route('/blog')
def blog():
    return 'Blog'

@app.route('/blog/<post_id>')
def blog_post(post_id):
    p = wirecat.posts.get_post(post_id)
    return render_template('post.html', post=p)

@app.route('/login')
def login():
    return render_template('login.html')


#-------------------------------------------------------------------------------------------------#
#   API~ Routes for api pages
#-------------------------------------------------------------------------------------------------#




@app.route('/api/v1')
def v1_help():
    #TODO
    #   return some json providing a top level overview of the api and how to use it
        return render_template('api-help.html')




#-------------------------------------------------------------------------------------------------#
#   ~API/AUTH~ Routes for api pages related to authorization of users
#-------------------------------------------------------------------------------------------------#


@app.route('/api/v1/auth/login', methods=['GET', 'POST'])
def login_api():
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/forum')

@app.route('/api/v1/auth/logout')

@app.route('/api/v1/auth/verify', methods = ['GET', 'POST'])
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

@app.route('/api/v1/posts')
def posts():
    #TODO:
    #   return json explaining how to auth and which child routes are available
    return ('post-help.html'), 200
@app.route('/api/v1/posts/add', methods=['GET','POST'])
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

@app.route('/api/v1/posts/delete', methods=['GET','POST'])
def delete():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/api/v1/posts/unpublish')

@app.route('/api/v1/posts/edit')

@app.route('/api/v1/posts/update')
def update_posts():
    """Update posts held in memory. This will initiate the pulling of content from the 
    data base and refreshing of the content lists that are held in memory"""
    if request.headers.get('auth') != s.get_author_key():
        return 'Forbidden', 403
    else:
        wirecat.posts.update(wirecat.db.get_recent_posts())
        return 'posts updated', 200

@app.route('/api/v1/posts/highlight')

@app.route('/api/v1/posts/highlight/add')

@app.route('/api/v1/posts/highlight/remove')

#-------------------------------------------------------------------------------------------------#
#   ERRORS~ - Routes for error pages
#-------------------------------------------------------------------------------------------------#

@app.errorhandler(404)
def err404(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)