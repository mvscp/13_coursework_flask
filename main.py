import json
import logging
import re
from flask import Flask, render_template, request, redirect
import utils

app = Flask(__name__)
logging.basicConfig(filename="logs/api.log", format="%(asctime)s [%(levelname)s] %(message)s", filemode="w")


@app.route("/", methods=['GET'])
def page_index():
    posts = utils.get_posts_all()
    bookmarks = utils.get_bookmark_posts()
    return render_template("index.html", posts=posts, bookmarks_count=len(bookmarks))


@app.route("/posts/<int:post_id>", methods=['GET'])
def page_post(post_id):
    comments = utils.get_comments_by_post_id(post_id)
    post = utils.get_post_by_pk(post_id)
    post_content = post['content']
    if "#" in post['content']:
        pattern = r"#\w*"
        tags = re.findall(pattern, post['content'])
        for tag in tags:
            html_tag = f'<a href="/tag/{tag[1:]}">{tag}</a>'
            post_content = post_content.replace(tag, html_tag, 1)
    return render_template("post.html", post=post, comments=comments, length=len(comments), post_content=post_content)


@app.route("/search/")
def page_search():
    s = request.args.get('s')
    if s:
        posts = utils.search_for_posts(s)
        return render_template("search.html", posts=posts, length=len(posts))


@app.route("/users/<string:username>")
def page_posts_by_user(username):
    posts = utils.get_posts_by_user(username)
    return render_template("user-feed.html", posts=posts, length=len(posts))


@app.errorhandler(404)
def page_error(exception):
    return f"Ошибка {exception}"


@app.errorhandler(500)
def page_error(exception):
    return f"Ошибка {exception}"


@app.route("/<string:page>.html")
def page_html(page):
    return render_template(f"{page}.html")


@app.route("/api/posts")
def page_posts_api():
    posts = utils.get_posts_all()
    logging.info('Запрос api/posts')
    return json.dumps(posts, ensure_ascii=False)


@app.route("/api/posts/<int:post_id>")
def page_post_api(post_id):
    post = utils.get_post_by_pk(post_id)
    logging.info(f'Запрос api/posts/{post_id}')
    return json.dumps(post, ensure_ascii=False)


@app.route("/bookmarks/add/<int:post_id>")
def add_bookmark(post_id):
    post = utils.get_post_by_pk(post_id)
    with open("data/bookmarks.json", "r", encoding="utf-8") as file:
        bookmarks = json.load(file)
        if not bookmarks.__contains__(post):
            bookmarks.append(post)
    with open("data/bookmarks.json", "w", encoding="utf-8") as file:
        json.dump(bookmarks, file, ensure_ascii=False, separators=(',\n', ': '))
    return redirect("/")


@app.route("/bookmarks/remove/<int:post_id>")
def remove_bookmark(post_id):
    post = utils.get_post_by_pk(post_id)
    with open("data/bookmarks.json", "r", encoding="utf-8") as file:
        bookmarks = json.load(file)
        if bookmarks.__contains__(post):
            bookmarks.remove(post)
    with open("data/bookmarks.json", "w", encoding="utf-8") as file:
        json.dump(bookmarks, file, ensure_ascii=False, separators=(',\n', ': '))
    return redirect("/")


@app.route("/bookmarks.html")
def page_bookmarks():
    posts = utils.get_bookmark_posts()
    return render_template("bookmarks.html", posts=posts)


@app.route("/tag/<string:tag_name>")
def page_search_by_tag(tag_name):
    posts = utils.get_posts_all()
    posts_by_tag = []
    for post in posts:
        if f"#{tag_name}" in post['content']:
            posts_by_tag.append(post)
    return render_template("tag.html", posts=posts_by_tag, tag=tag_name)


if __name__ == '__main__':
    app.run()
