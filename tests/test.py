"""
Модуль для тестирования проекта
"""


from fastapi.testclient import TestClient
import faker
from app.main import app

client = TestClient(app)
fake = faker.Faker()

client.fake_user_email = fake.email()
client.fake_user_password = fake.password()
client.fake_user_name = fake.first_name()
client.new_user_id = 0
client.auth_token = ""


def test_signup():
    """Тестирование создания пользователя"""
    response = client.post("/auth/signup",
                           json={"email": client.fake_user_email,
                                 "password": client.fake_user_password,
                                 "name": client.fake_user_name}
    )
    assert response.status_code == 201
    client.new_user_id = response.json()


def test_login():
    """Тестирование входа в систему"""
    response = client.post("/auth/login",
                           data={"username": client.fake_user_email,
                                 "password": client.fake_user_password}
    )
    assert response.status_code == 200
    client.auth_token = response.json()['access_token']


def test_me():
    """Тестирование получения текущего пользователя"""
    response = client.get("/utils/me", headers={"Authorization": f"Bearer {client.auth_token}"})
    assert response.status_code == 200
    assert response.json() == client.new_user_id

def test_books():
    """Тестирование добавления книги"""
    respose = client.post("/books", json={"title": "История господина Н",
        "author": "Некто Нектонович",
        "year": 2001})
    assert respose.status_code == 201

def test_get_book():
    """Тестирование выдачи книги"""
    login_response = client.post(
        "/token",
        data={"username": "tester@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    responce = client.post("/book_ownship/add", data={"book_name":"История господина Н"}, 
                           headers={"Authorization": f"Bearer {token}"})
    assert responce.status_code == 200
