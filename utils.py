import json


def get_posts_all() -> list:
    with open("data/posts.json", "r", encoding="utf-8") as file:
        posts = json.load(file)
    return posts


def get_bookmark_posts() -> list:
    with open("data/bookmarks.json", "r", encoding="utf-8") as file:
        posts = json.load(file)
    return posts


def get_posts_by_user(user_name: str) -> list:
    posts = get_posts_all()
    posts_by_user = []
    allowed_user_names = set(post['poster_name'] for post in posts)
    if user_name not in allowed_user_names:
        raise ValueError
    for post in posts:
        if post['poster_name'] == user_name.lower():
            posts_by_user.append(post)
    return posts_by_user


def get_comments_by_post_id(post_id: int) -> list:
    with open("data/comments.json", "r", encoding="utf-8") as file:
        comments = json.load(file)
    allowed_post_id = set(comment['post_id'] for comment in comments)
    comments_by_post_id = []
    if post_id not in allowed_post_id:
        raise ValueError
    for comment in comments:
        if post_id == comment['post_id']:
            comments_by_post_id.append(comment)
    return comments_by_post_id


def search_for_posts(query: str) -> list:
    posts = get_posts_all()
    posts_with_query = []
    for post in posts:
        if query in post['content'].lower():
            posts_with_query.append(post)
    return posts_with_query


def get_post_by_pk(pk: int) -> dict:
    posts = get_posts_all()
    return posts[pk-1]
