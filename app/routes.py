from flask import Flask, render_template
import os
from app import app
from app.util.wirecat import WireCat

wirecat = WireCat()

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

