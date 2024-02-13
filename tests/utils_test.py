import pytest
import utils

post_keys_should_be = {'poster_name', 'poster_avatar', 'pic', 'content', 'views_count', 'likes_count', 'pk'}
comment_keys_should_be = {'post_id', 'commenter_name', 'comment', 'pk'}


def test_get_posts_all():
    posts = utils.get_posts_all()
    assert type(posts) is list, "Возвращается не список"
    assert len(posts) > 0, "Возвращает пустой список"
    assert set(posts[0].keys()) == post_keys_should_be, "У постов неверные ключи"


def test_get_posts_by_user():
    posts = utils.get_posts_by_user("leo")
    with pytest.raises(ValueError):
        utils.get_posts_by_user("gdfgs")
    if len(posts) > 0:
        assert set(posts[0].keys()) == post_keys_should_be, "У постов неверные ключи"
    assert type(posts) is list, "Возвращается не список"


def test_get_comments_by_post_id():
    comments = utils.get_comments_by_post_id(1)
    with pytest.raises(ValueError):
        utils.get_comments_by_post_id(-24)
    if len(comments) > 0:
        assert set(comments[0].keys()) == comment_keys_should_be, "У комментариев неверные ключи"
    assert type(comments) is list, "Возвращается не список"


def test_search_for_posts():
    posts = utils.search_for_posts("еда")
    assert type(posts) is list, "Возвращается не список"
    if len(posts) > 0:
        assert set(posts[0].keys()) == post_keys_should_be, "У постов неверные ключи"


def test_get_post_by_pk():
    post = utils.get_post_by_pk(1)
    assert type(post) is dict, "Возвращается не словарь"
    assert set(post.keys()) == post_keys_should_be, "У поста неверные ключи"
