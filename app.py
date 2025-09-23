
from typing import List, Dict, Optional
from flask import Flask, render_template, request, redirect, url_for
from flask.typing import ResponseReturnValue
from flask import Flask, render_template, request, redirect, url_for
import json

JSON_PATH = 'data/storage.json'

app = Flask(__name__)


@app.route('/')
def hello_world() -> str:
    """
    Render the main blog page with all posts.

    Returns:
        str: Rendered HTML for the main page.
    """
    with open('data/storage.json', 'r') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add() -> ResponseReturnValue:
    """
    Handle adding a new blog post.

    GET: Show the add form.
    POST: Save the new post and redirect.

    Returns:
        ResponseReturnValue: Rendered HTML or redirect response.
    """
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
def delete(post_id: int) -> ResponseReturnValue:
    """
    Delete a blog post by its ID and redirect to the main page.

    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        ResponseReturnValue: Redirect response to the main page.
    """
    blog_posts = open_file()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    write_file(blog_posts)  
    return redirect('/')



@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id: int) -> ResponseReturnValue:
    """
    Update an existing blog post.

    GET: Show the update form.
    POST: Save the changes and redirect.

    Args:
        post_id (int): The ID of the post to update.

    Returns:
        ResponseReturnValue: Rendered HTML or redirect response.
    """
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
    else:
        return render_template('update.html', post=post)

def open_file() -> List[Dict]:
    """
    Read all blog posts from the JSON storage file.

    Returns:
        List[Dict]: List of all blog posts.
    """
    with open(JSON_PATH, 'r') as f:
        post_list: List[Dict] = json.load(f)
    return post_list

def write_file(post_list: List[Dict]) -> None:
    """
    Write the list of blog posts to the JSON storage file.

    Args:
        post_list (List[Dict]): The list of blog posts to write.
    """
    with open(JSON_PATH, 'w') as f:
        json.dump(post_list, f, indent=4)

def fetch_post_by_id(post_id: int) -> Optional[Dict]:
    """
    Fetch a single blog post by its ID.

    Args:
        post_id (int): The ID of the post to fetch.

    Returns:
        Optional[Dict]: The post dict if found, otherwise None.
    """
    blog_posts = open_file()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)