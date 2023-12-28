"""
All sections of this page are tagged with the following titles in order to be easily 
searchable. MAIN~,API~, etc.

Sections:
    MAIN~
    API~
    ERRORS~

    love, 
        mimi
"""
import os
from flask import Flask, render_template, request
from app import app
from app.util.wirecat import WireCat
from app.util.w_secrets import Secrets

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
    return 'Downloads'

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

# @app.route('/blog/add', methods=['POST', 'GET'])
# def add_post():
#     if request.headers.get('auth') != s.get_author_key():
#         return 'Forbidden', 403
#     elif request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
#         return f"Post added\nDATA: {request.get_json()}"
#     else:
#         return 'Error: Post add failed', 404

# @app.route('/blog/edit/<post_id>')
# def edit_post():
#     return f"Post {post_id} edited"

# @app.route('/blog/delete/<post_id>')
# def delete_post():
#     return f"Post {post_id} deleted"

# @app.route('/blog/update')
# def update_posts():
#     if request.headers.get('auth') != s.get_author_key():
#         return 'Forbidden', 403
#     else:
#         wirecat.posts.update(wirecat.db.get_recent_posts())
#         return 'posts updated', 200

#-------------------------------------------------------------------------------------------------#
#   API~ - Routes for api pages
#-------------------------------------------------------------------------------------------------#

@app.route('/api/v1')
def v1_help():
    #TODO
    #   return some json providing a top level overview of the api and how to use it
        return render_template('api-help.html')

@app.route('/api/v1/auth/login')

@app.route('/api/v1/auth/logout')

@app.route('/api/v1/auth/verify')
def verify():
    #TODO
    #Verify requests that use api keys/HMAC and not a login system
    return 'Success', 200
@app.route('/api/v1/posts')
def posts():
    #TODO:
    #   return json explaining how to auth and which child routers are available
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

@app.route('/api/v1/posts/update', methods=['GET','POST'])

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