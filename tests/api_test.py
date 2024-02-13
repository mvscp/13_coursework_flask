import json

keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}


def test_all_posts(test_client):
    response = test_client.get("/api/posts", follow_redirects=True)
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200, "Статус код всех постов неверен"
    assert type(data) is list, "Возвращается не список"
    assert set(data[0].keys()) == keys, "Неверные ключи"


def test_post(test_client):
    response = test_client.get("/api/post/1", follow_redirects=True)
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200, "Статус код поста неверен"
    assert type(data) is dict, "Возвращается не словарь"
    assert set(data.keys()) == keys, "Неверные ключи"
