from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    best = get_best_posts()
    return render_template('frontpage.html', best_posts=best)


def get_best_posts():
    posts = []
    for d in os.listdir("static/posts"):
        if not os.path.exists(f'static/posts/{d}/{d}.jpg'):
            image = f'static/images/defaultpost.jpg'
        else:
            image = f'static/posts/{d}/{d}.jpg'
        text = open(f'static/posts/{d}/{d}.txt').read()
        posts.append({"text": text, "image": image})

    return posts

if __name__ == '__main__':
    app.run(debug=True)