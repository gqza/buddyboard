
from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
import os
import json
import uuid
from dotenv import load_dotenv, dotenv_values 
# from werkzeug.routing import IntegerConverter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app)
load_dotenv()

database = os.getenv("DATABASE")
    
def postsExist():
    try:
        with open(os.getenv("DATABASE"), 'a') as f:
            pass 
    except IOError as e:
        print(f"Error ensuring posts exist: {e}")

@app.before_request
def before_request():
    postsExist()

@app.route('/', methods=['GET'])
def index():
    try:
        with open(database, "r", encoding='utf-8') as data:
            posts = json.load(data)
    except FileNotFoundError:
        print("posts.json not found, starting fresh.")
    except Exception as e:
        print(f"Error reading posts.json: {e}")
        return "An error occurred while loading posts. Please try again later.", 500

    return render_template("main.html", posts=posts, proxy=os.getenv("PROXY"))

@app.route('/reply/<post_id>', methods=['GET'])
def replyIndex(post_id):
    try:
        with open(database, "r", encoding='utf-8') as data:
            replies = json.load(data)
    except FileNotFoundError:
        print("posts.json not found, starting fresh.")
    except Exception as e:
        print(f"Error reading posts.json: {e}")
        return "An error occurred while loading posts. Please try again later.", 500
    
    parent_post = next((p for p in replies if p.get('id') == post_id), None)
    if parent_post is None:
        return "Post not found", 404

    return render_template('reply.html', post=parent_post, replies=replies, proxy=os.getenv("PROXY"))

@app.route('/vote/<post>/<int(signed=True):rating>', methods=['POST'])
@limiter.limit("8/day", key_func=get_remote_address)
def rate(post, rating):
    try:
        with open(database, "r+", encoding='utf-8') as data:
            posts = json.load(data)
            found = False
            for i in posts:
                if i['id'] == post:
                    i['yeahs'] += rating
                    found = True
                    break

            if not found: 
                data = {
                    "status": 404
                }
                return data    

            data.seek(0)
            json.dump(posts, data, indent=4)
            data = {
                "status": 200
            }
            return data
    except Exception as e:
        print(f"Error reading posts.json: {e}")
        return "An error occurred while loading posts. Please try again later.", 500

@app.route('/reply/<post_id>', methods=['POST'])
@app.route('/', methods=['POST'])
def add_data(post_id=None):

    post = {}
    post['id'] = str(uuid.uuid1())
    post['user'] = request.form.get('user', '').strip() or 'anon'
    post['content'] = escape(request.form.get('data', ''))
    post['yeahs'] = 0
    post['replying'] = post_id or None
    post['image'] = request.form.get('image', '') or None

    if not post:
        return "Say something!", 400
    

    final_user_name = post['user'] if post['user'] else 'anon'
    try:
        with open(database, "r+", encoding='utf-8') as read:
            file = json.load(read)
            file.append(post) 
        with open(database, "w", encoding='utf-8') as write:
            json.dump(file, write, indent=4)
        return redirect(request.path)
    except Exception as e:
        print(f"Error writing to posts.json: {e}")
        return "An error occurred while saving your post. Please try again.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
