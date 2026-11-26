import pytest
import requests

"""
Вариант 1
Использовать сервис
https://restful-booker.herokuapp.com
Документация:
https://restful-booker.herokuapp.com/apidoc/ 
Задача: Написать авто тесты используя ПОМ, в котором будет проверяться создание брони, частичное изменение брони, 
создание брони, а также любой негативный сценарий на ваш выбор
"""

# --- API Client (аналог Page Object Model для API) ---
class BookingClient:
    BASE_URL = "https://restful-booker.herokuapp.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def get_auth_token(self, username="admin", password="password123"):
        """Получение токена авторизации для операций изменения/удаления"""
        response = self.session.post(
            f"{self.BASE_URL}/auth",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        return response.json()["token"]

    def create_booking(self, payload: dict):
        """Создание нового бронирования (POST /booking)"""
        return self.session.post(f"{self.BASE_URL}/booking", json=payload)

    def get_booking(self, booking_id: int):
        """Получение информации о брони по ID (GET /booking/:id)"""
        return self.session.get(f"{self.BASE_URL}/booking/{booking_id}")

    def partial_update_booking(self, booking_id: int, payload: dict, token: str = None):
        """Частичное обновление брони (PATCH /booking/:id)"""
        headers = {}
        if token:
            headers["Cookie"] = f"token={token}"
        return self.session.patch(
            f"{self.BASE_URL}/booking/{booking_id}",
            json=payload,
            headers=headers
        )

    def delete_booking(self, booking_id: int, token: str):
        """Удаление брони (DELETE /booking/:id)"""
        headers = {"Cookie": f"token={token}"}
        return self.session.delete(
            f"{self.BASE_URL}/booking/{booking_id}",
            headers=headers
        )


# --- Фикстуры Pytest ---
@pytest.fixture
def client():
    return BookingClient()


@pytest.fixture
def booking_data():
    return {
        "firstname": "Ivan",
        "lastname": "Ivanov",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-10"
        },
        "additionalneeds": "Breakfast"
    }


# --- Автотесты ---
def test_create_booking(client, booking_data):
    """1. Позитивный тест: создание бронирования"""
    response = client.create_booking(booking_data)
    assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

    data = response.json()
    assert "bookingid" in data, "В ответе отсутствует bookingid"
    assert data["booking"] == booking_data, "Данные созданной брони не совпадают с отправленными"


def test_partial_update_booking(client, booking_data):
    """2. Позитивный тест: частичное изменение брони (PATCH)"""
    # Сначала создаем бронь и получаем токен
    booking_id = client.create_booking(booking_data).json()["bookingid"]
    token = client.get_auth_token()

    # Меняем только имя и цену
    patch_payload = {
        "firstname": "Petr",
        "totalprice": 250
    }
    response = client.partial_update_booking(booking_id, patch_payload, token=token)
    assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

    updated_data = response.json()
    assert updated_data["firstname"] == "Petr"
    assert updated_data["totalprice"] == 250
    # Проверяем, что остальные поля не затерлись
    assert updated_data["lastname"] == booking_data["lastname"]


def test_delete_booking(client, booking_data):
    """3. Позитивный тест: удаление бронирования"""
    booking_id = client.create_booking(booking_data).json()["bookingid"]
    token = client.get_auth_token()

    delete_response = client.delete_booking(booking_id, token=token)
    assert delete_response.status_code == 201, f"Ожидался код 201, получен {delete_response.status_code}"

    # Проверяем, что после удаления бронь больше не находится (404)
    get_response = client.get_booking(booking_id)
    assert get_response.status_code == 404


def test_partial_update_without_auth_negative(client, booking_data):
    """4. Негативный тест: попытка частичного изменения брони без авторизации"""
    booking_id = client.create_booking(booking_data).json()["bookingid"]

    patch_payload = {"firstname": "Hacker"}
    # Вызываем PATCH без передачи token
    response = client.partial_update_booking(booking_id, patch_payload, token=None)

    assert response.status_code == 403, f"Ожидался статус 403 Forbidden, получен {response.status_code}"