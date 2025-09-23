from flask import Flask, render_template, request, redirect, url_for
import json

JSON_PATH = 'data/storage.json'

app = Flask(__name__)


@app.route('/')
def hello_world():
    with open('data/storage.json', 'r') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = open_file()
        new_post = {
            "id": len(blog_posts) + 1,
            "author": request.form['author'],
            "title": request.form['title'],
            "content": request.form['your_post']}
        blog_posts.append(new_post)
        write_file(blog_posts)
        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = open_file()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    write_file(blog_posts)  
    return redirect('/')



@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404
    
    if request.method == 'POST':
        blog_posts = open_file()
        for post in blog_posts:
            if post['id'] == post_id:
                post['author'] = request.form['author']
                post['title'] = request.form['title']
                post['content'] = request.form['your_post']
        write_file(blog_posts) 
        return redirect('/')
    
    # Else, it's a GET request
    # So display the update.html page
    else:
        return render_template('update.html', post=post)

def open_file() -> list:
    with open(JSON_PATH, 'r') as f:
        post_list = json.load(f)
    return post_list

def write_file(post_list:list) -> None:
    with open(JSON_PATH, 'w') as f:
        json.dump(post_list, f, indent=4)

def fetch_post_by_id(post_id: int):
    blog_posts = open_file()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)