from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    with open('data/storage.json', 'r') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)