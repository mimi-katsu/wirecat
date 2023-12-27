"""
Sections:
    MAIN~
    ERRORS~
"""

from flask import Flask, render_template, request
import os
from app import app
from app.util.wirecat import WireCat
from app.util.w_secrets import Secrets

wirecat = WireCat()
wirecat.posts.update(wirecat.db.get_recent_posts())
s = Secrets()

# ------------------------------------------------------------------------------
#   MAIN~ - Routes for main pages
#-------------------------------------------------------------------------------


@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    
    best = wirecat.db.get_recent_posts()
    latest  = best[0]
    return render_template('frontpage.html', best_posts=best, latest_post=latest)

@app.route('/downloads')
def downloads():
    return 'Downloads'

@app.route('/community')
def community():
    return 'Community'

@app.route('/blog')
def blog():
    return 'Blog'

@app.route('/blog/<post_id>')
def blog_post(post_id):
    p = wirecat.posts.get_post(post_id)
    return render_template('post.html', post=p)

@app.route('/blog/add', methods=['POST', 'GET'])
def add_post():
    if request.headers.get('auth') != s.get_author_key():
        return 'Forbidden', 403
    elif request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        return f"Post added\nDATA: {request.get_json()}"
    else:
        return 'Error: Post add failed', 404

@app.route('/blog/edit/<post_id>')
def edit_post():
    return f"Post {post_id} edited"

@app.route('/blog/delete/<post_id>')
def delete_post():
    return f"Post {post_id} deleted"

@app.route('/blog/update')
def update_posts():
    if request.headers.get('auth') != s.get_author_key():
        return 'Forbidden', 403
    else:
        wirecat.posts.update(wirecat.db.get_recent_posts())
        return 'posts updated', 200

# ------------------------------------------------------------------------------
#   API~ - Routes for api pages
#-------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
#   ERRORS~ - Routes for error pages
#-------------------------------------------------------------------------------

@app.errorhandler(404)
def err404(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)