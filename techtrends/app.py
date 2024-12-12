
import sqlite3
import os
from werkzeug.exceptions import abort
from datetime import datetime
import logging
import sys
from flask import Flask, render_template, request, url_for, redirect, flash

app = Flask(__name__)
app.config['connection_count'] = 0

# Initialize logger to write to STDOUT and STDERR
def initialize_logger():
    log_level = os.getenv("LOGLEVEL", "DEBUG").upper()
    log_level = (
        getattr(logging, log_level)
        if log_level in ["CRITICAL", "DEBUG", "ERROR", "INFO", "WARNING"]
        else logging.DEBUG
    )

    logger = logging.getLogger()
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s, %(message)s')
    
    # Log to STDOUT
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    
    # Log to STDERR
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)  # Only errors to STDERR
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

initialize_logger()

def get_db_connection():
    try:
        if os.path.exists("database.db"):
            connection = sqlite3.connect("database.db")
        else:
            raise RuntimeError('Failed to open DB')
    except sqlite3.OperationalError:
        logging.error('Database.db is not properly defined. Run init_db.py!')

    connection.row_factory = sqlite3.Row
    app.config['connection_count'] = app.config['connection_count'] + 1
    return connection


def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    connection.close()
    return post


# Define the main route of the web application
@app.route("/")
def index():
    connection = get_db_connection()
    posts = connection.execute("SELECT * FROM posts").fetchall()
    connection.close()
    return render_template("index.html", posts=posts)


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    if post is None:
        logging.error('404 Error: Article with id %s does not exist!', post_id)
        return render_template("404.html"), 404
    else:
        logging.debug('Article "%s" accessed.', post["title"])
        return render_template("post.html", post=post)


# Define the About Us page
@app.route("/about")
def about():
    logging.debug("About Us page accessed.")
    return render_template("about.html")


# Define the post creation functionality
@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            connection = get_db_connection()
            connection.execute(
                "INSERT INTO posts (title, content) VALUES (?, ?)", (title, content)
            )
            connection.commit()
            connection.close()
            logging.debug('New article "%s" created.', title)
            return redirect(url_for("index"))
    return render_template("create.html")


# Define healthz endpoint
@app.route("/healthz")
def healthz():
    try:
        connection = get_db_connection()
        connection.cursor()
        connection.execute("SELECT * FROM posts")
        connection.close()
        return {"result": "OK - healthy"}
    except Exception:
        return {"result": "ERROR - unhealthy"}, 500


# Define metrics endpoint
@app.route("/metrics")
def metrics():
    connection = get_db_connection()
    posts = connection.execute("SELECT * FROM posts").fetchall()
    connection.close()
    post_count = len(posts)
    data = {"db_connection_count": app.config['connection_count'], "post_count": post_count}
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3111")