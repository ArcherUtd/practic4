import pytest
from datetime import datetime
from httpx import AsyncClient
from fastapi import FastAPI, HTTPException
from main import app, ALPHABET, users, methods_of_encryption, sessions, identification_user, encrypt_cesar_method, decrypt_cesar_method, encrypt_vigenere_method, decrypt_vigenere_method, hack_text

# Этот адрес нужно заменить на URL вашего FastAPI приложения
BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
def client():
    return AsyncClient(app=app, base_url=BASE_URL)


# Тест для добавления пользователей
@pytest.mark.asyncio
async def test_append_user(client):
    new_users = [
        {"login": "TestUser1", "secret": "TestSecret1"},
        {"login": "TestUser2", "secret": "TestSecret2"},
    ]
    response = await client.post("/user", json=new_users)
    assert response.status_code == 200
    assert response.json()[-2:] == new_users  # Проверяем, что последние два пользователя добавлены


# Тест для получения списка пользователей
@pytest.mark.asyncio
async def test_get_list_users(client):
    response = await client.get("/list_users")
    assert response.status_code == 200
    assert all("secret" not in user for user in response.json())  # Проверяем, что в ответе нет секретов


# Тест для получения списка методов шифрования
@pytest.mark.asyncio
async def test_get_methods(client):
    response = await client.get("/get_methods")
    assert response.status_code == 200
    assert response.json() == methods_of_encryption


# Тест для шифрования методом Цезаря
@pytest.mark.asyncio
async def test_encrypt_cesar_method(client):
    text_for_encrypt = "ПРИВЕТ"
    number_of_shifts = 3
    expected_encrypted_text = "МНЁ9ВП"
    response = await client.get(f"/encrypt/cesar?text_for_encrypt={text_for_encrypt}&number_of_shifts={number_of_shifts}")
    assert response.status_code == 200
    assert response.text == expected_encrypted_text


# Тест для дешифрования методом Цезаря
@pytest.mark.asyncio
async def test_decrypt_cesar_method(client):
    text_for_decrypt = "МНЁ9ВП"
    number_of_shifts = 3
    expected_decrypted_text = "ПРИВЕТ"
    response = await client.get(f"/decrypt/cesar?text_for_decrypt={text_for_decrypt}&number_of_shifts={number_of_shifts}")
    assert response.status_code == 200
    assert response.text == expected_decrypted_text


# Тест для шифрования методом Виженера
@pytest.mark.asyncio
async def test_encrypt_vigenere_method(client):
    text_for_encrypt = "ПРИВЕТ"
    keyword = "КЛЮЧ"
    expected_encrypted_text = "46Ж3,8"
    response = await client.get(f"/encrypt/vigenere?text_for_encrypt={text_for_encrypt}&keyword={keyword}")
    assert response.status_code == 200
    assert response.text == expected_encrypted_text


# Тест для дешифрования методом Виженера
@pytest.mark.asyncio
async def test_decrypt_vigenere_method(client):
    text_for_decrypt = "46Ж3,8"
    keyword = "КЛЮЧ"
    expected_decrypted_text = "ПРИВЕТ"
    response = await client.get(f"/decrypt/vigenere?text_for_decrypt={text_for_decrypt}&keyword={keyword}")
    assert response.status_code == 200
    assert response.text == expected_decrypted_text


# Тест для взлома методом Цезаря
@pytest.mark.asyncio
async def test_break_cesar_with_known_part(client):
    text_for_hack = "МНЁ9ВП"
    known_word = "ПРИВЕТ"
    expected_method = "cesar"
    expected_shift = 3
    expected_decrypted_text = "ПРИВЕТ"
    response = await client.post("/break", json={"text_for_hack": text_for_hack, "known_word": known_word})
    assert response.status_code == 200
    assert response.json()["method"] == expected_method
    assert response.json()["shift"] == expected_shift
    assert response.json()["decrypted_text"] == expected_decrypted_text


# Тест для взлома методом Виженера
@pytest.mark.asyncio
async def test_break_vigenere_with_known_key_part(client):
    text_for_hack = "-Э.6К9ЬБЬ1А5Ь6С6Ё"
    known_word = "КАРЛ"
    expected_method = "vigenere"
    expected_keyword = "КЛАР"
    expected_decrypted_text = "КАРЛ УКРАЛ КАРАЛЫ"
    response = await client.post("/break", json={"text_for_hack": text_for_hack, "known_word": known_word})
    assert response.status_code == 200
    assert response.json()["method"] == expected_method
    assert response.json()["keyword"] == expected_keyword
    assert response.json()["decrypted_text"] == expected_decrypted_text


# Тест для получения сессии по ID
@pytest.mark.asyncio
async def test_get_session(client):
    session_id = 1
    login = "IgorKrutyi"
    secret = "KalinaNEsport"
    expected_session = {
        "id": 1,
        "user_id": 1,
        "method_id": 1,
        "data_in": "ПРИВЕТ",
        "params": {"text": "ПРИВЕТ", "shifts": 3},
        "data_out": "МНЁ9ВП",
        "status": 200,
        "created_at": "2024-06-16 15:34:12.345678",
        "time_op": 0.21,
    }
    response = await client.get(f"/get_session/{session_id}", params={"login": login, "secret": secret})
    assert response.status_code == 200
    assert response.json() == expected_session


#запуск всех тестов
if __name__ == "__main__":
    pytest.main()
