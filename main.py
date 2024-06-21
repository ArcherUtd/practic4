from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

ALPHABET = " ,.:(_)-0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

app = FastAPI(
    title='ServiceForEncryptingByArcher'
)

class User(BaseModel):
    login: str
    secret: str


class Methods(BaseModel):
    id: int
    caption: str
    json_params: dict
    description: str


class Sessions(BaseModel):
    id: int
    user_id: int
    method_id: int
    data_in: str
    params: str
    data_out: str
    status: str
    created_at: datetime
    time_op: datetime

users=[
    {"login": "IgorKrutyi", "secret": "KalinaNEsport"},
    {"login": "StasGod", "secret": "OpelSila"},
    {"login": "DaniilSolaris", "secret": "WestGym"},
    {"login": "MironAlkash", "secret": "smrirno"},

]


methods_of_encryption=[
    {"id": 1, "caption": "Метод Цезаря", "json_params": {"text": "str", "shifts": "int"}, "description": "Шифруется методом сдвига"},
    {"id": 2, "caption": "Метод Виженера", "json_params": {"text": "str", "key": "str"}, "description": "Метод полиалфавитного шифрования с использованием ключевого слова"},
]


@app.post("/user")
def append_user(user: List[User]):
    users.extend(user)
    return users


@app.get("/list_users")
def get_list_users():
    users_without_secret = []
    for user in users:
        new_user = {}
        for key, value in user.items():
            if key != "secret":
                new_user[key] = value
    return users_without_secret


@app.get("/get_methods")
def get_methods():
    return methods_of_encryption


@app.get("/encrypt/cesar")
def encrypt_cesar_method(text_for_encrypt: str, number_of_shifts: int):
    text_for_encrypt_upper = text_for_encrypt.upper()
    encrypted_text = []
    alphabet_size = len(ALPHABET)

    for char in text_for_encrypt_upper:
        if char in ALPHABET:
            original_index = ALPHABET.index(char)
            new_index = (original_index + number_of_shifts) % alphabet_size
            encrypted_text.append(ALPHABET[new_index])
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)


@app.get("/decrypt/cesar")
def decrypt_cesar_method(text_for_decrypt: str, number_of_shifts: int):
    text_for_decrypt_upper = text_for_decrypt.upper()
    decrypted_text = []
    alphabet_size = len(ALPHABET)

    for char in text_for_decrypt_upper:
        if char in ALPHABET:
            encrypted_index = ALPHABET.index(char)
            new_index = (encrypted_index - number_of_shifts) % alphabet_size
            decrypted_text.append(ALPHABET[new_index])
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)


@app.get("/encrypt/vigenere")
def encrypt_vigenere_method(text_for_encrypt: str, keyword: str):
    text_for_encrypt_upper = text_for_encrypt.upper()
    keyword_upper = keyword.upper()
    encrypted_text = []
    alphabet_size = len(ALPHABET)
    keyword_len = len(keyword_upper)

    for i, char in enumerate(text_for_encrypt_upper):
        if char in ALPHABET:
            original_index = ALPHABET.index(char)
            key_char = keyword_upper[i % keyword_len]
            key_index = ALPHABET.index(key_char)
            new_index = (original_index + key_index) % alphabet_size
            encrypted_text.append(ALPHABET[new_index])
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)


@app.get("/decrypt/vigenere")
def decrypt_vigenere_method(text_for_decrypt: str, keyword: str):
    text_for_decrypt_upper = text_for_decrypt.upper()
    keyword_upper = keyword.upper()
    decrypted_text = []
    alphabet_size = len(ALPHABET)
    keyword_len = len(keyword_upper)

    for i, char in enumerate(text_for_decrypt_upper):
        if char in ALPHABET:
            encrypted_index = ALPHABET.index(char)
            key_char = keyword_upper[i % keyword_len]
            key_index = ALPHABET.index(key_char)
            new_index = (encrypted_index - key_index) % alphabet_size
            decrypted_text.append(ALPHABET[new_index])
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)