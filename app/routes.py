from flask import Flask, render_template, request
import os
from app import app
from app.util.wirecat import WireCat

wirecat = WireCat()
wirecat.posts.update(wirecat.db.get_recent_posts())

@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    best = wirecat.db.get_recent_posts()
    return render_template('frontpage.html', best_posts=best)

@app.route('/downloads')
def downloads():
    return 'Downloads'

@app.route('/community')
def community():
    return 'Community'
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/blog')
def blog():
    return 'BLog'

@app.route('/blog/<post_id>')
def blog_post(post_id):
    p = wirecat.posts.get_post(post_id)
    return render_template('post.html', post=p)

@app.route('/blog/add', methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':

        return f"Post added\nDATA: {request.get_json()}"
    else:
        return 'Error: Post add failed', 403

@app.route('/blog/edit/<post_id>')
def edit_post():
    return f"Post {post_id} edited"

@app.route('/blog/delete/<post_id>')
def delete_post():
    return f"Post {post_id} deleted"

@app.route('/blog/update')
def update_posts():
    wirecat.posts.update(wirecat.db.get_recent_posts())
    return 'posts updated', 200