import pymysql
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from password import password

from flask_ckeditor import CKEditor, CKEditorField

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DATABASE
db = pymysql.connect(host="localhost", user="root", password=password, database="updatedmovieblog")
cursor = db.cursor()


def insert_data(id, title, subtitle, date, body, author, img_url):
    sql = "INSERT INTO BlogPost (id, title, subtitle, date, body, author, img_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (id, title, subtitle, date, body, author, img_url)
    cursor.execute(sql, values)
    db.commit()
    print("movie inserted successfully.")


def retrieve_all_posts():
    posts = []
    db = pymysql.connect(host="localhost", user="root", password="mysql@123", database="updatedmovieblog")
    cursor = db.cursor()

    try:
        query = "SELECT * FROM blogpost"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            post = {
                "id": row[0],
                "title": row[1],
                "subtitle": row[2],
                "date": row[3],
                "body": row[4],
                "author": row[5],
                "img_url": row[6]
            }
            posts.append(post)
    except pymysql.Error as e:
        print(f"Error while retrieving data: {e}")
    finally:
        db.close()
    return posts


@app.route('/')
def index():
    posts = retrieve_all_posts()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = None
    all_posts = retrieve_all_posts()
    for post in all_posts:
        if post["id"] == post_id:
            requested_post = post
            break

    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        return "Post created successfully"

    # If it's a GET request, render the template
    requested_post = retrieve_all_posts()
    return render_template("post.html", post=requested_post)


@app.route("/edit/<int:post_id>")
def edit(post_id):
    requested_post = None
    all_posts = retrieve_all_posts()
    for post in all_posts:
        if post["id"] == post_id:
            requested_post = post
            break

    return render_template("make-post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
