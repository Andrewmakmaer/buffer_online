from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_key():
    response = client.post(
        "/app",
        headers={"X-Token": "coneofsilence"},
        json={"id": "add_text", "text": "Foo Bar", "key": 0},
    )
    assert response.status_code == 200
    assert int(response.text)
    return int(response.text)


some_key = test_create_key()


def test_correct_post():
    response = client.post(
        "/app",
        headers={"X-Token": "coneofsilence"},
        json={"id": "get_text", "key": some_key},
    )
    assert response.status_code == 200
    assert response.text == '"Foo Bar"'


test_correct_post()


def test_bad_post():
    response = client.post(
        "/app",
        headers={"X-Token": "coneofsilence"},
        json={"id": "something", "text": "Foo Bar", "key": 0},
    )
    assert response.status_code == 400


test_bad_post()


def test_adverb_bad_post():
    response = client.post(
        "/app",
        headers={"X-Token": "coneofsilence"},
        json={"text": "Foo Bar", "key": 0},
    )
    assert response.status_code == 422


test_adverb_bad_post()
