import sqlite3
import logging
from datetime import datetime
from flask import Flask, flash, render_template, request, url_for, redirect
import os

# Global variable to track database connection count
connection_count = 0

def get_db_connection():
    """Establishes a connection to the database."""
    global connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection_count += 1
    return connection

def get_post(post_id):
    """Retrieves a post by its ID from the database."""
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    connection.close()
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    """Displays all posts."""
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    """Displays the About page."""
    log_message('About page accessed')
    return render_template('about.html')

@app.route('/<int:post_id>')
def post(post_id):
    """Displays a specific post."""
    post = get_post(post_id)
    if post is None:
        log_message(f'Post with ID "{post_id}" does not exist')
        return render_template('404.html'), 404
    else:
        log_message(f'Post "{post["title"]}" retrieved')
        return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    """Handles the creation of new posts."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            connection.commit()
            connection.close()
            log_message(f'Post "{title}" created')
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/metrics')
def metrics():
    """Returns application metrics such as database connection count and post count."""
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    post_count = len(posts)
    return {"db_connection_count": connection_count, "post_count": post_count}

@app.route('/healthz')
def healthz():
    """Liveness endpoint to verify application is running."""
    return {"result": "OK - application is running"}, 200

@app.route('/readiness')
def readiness():
    """Readiness endpoint to verify database connectivity."""
    try:
        connection = get_db_connection()
        connection.execute('SELECT 1')  # Simple query to verify database connection
        connection.close()
        return {"result": "OK - ready"}, 200
    except Exception as e:
        log_message(f'Readiness check failed: {str(e)}')
        return {"result": "ERROR - database not ready"}, 500

def log_message(msg):
    """Logs a message with a timestamp."""
    app.logger.info(f'{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} | {msg}')

def init_db():
    """Initializes the database if it doesn't already exist."""
    if not os.path.exists('database.db'):
        connection = sqlite3.connect('database.db')
        with open('schema.sql') as f:
            connection.executescript(f.read())
        connection.close()

if __name__ == "__main__":
    init_db()
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=3111)
