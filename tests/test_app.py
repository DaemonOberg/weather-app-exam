import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to my weather app!" in response.data
