from datetime import datetime
from http.client import HTTPException
from typing import List, Dict
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
    params: dict
    data_out: str
    status: int
    created_at: datetime
    time_op: float


users = [
    {"id": 1, "login": "IgorKrutyi", "secret": "KalinaNEsport"},
    {"id": 2, "login": "StasGod", "secret": "OpelSila"},
    {"id": 3, "login": "DaniilSolaris", "secret": "WestGym"},
    {"id": 4, "login": "MironAlkash", "secret": "smrirno"},
]

methods_of_encryption = [
    {"id": 1, "caption": "Метод Цезаря", "json_params": {"text": "str", "shifts": "int"},
     "description": "Шифруется методом сдвига"},
    {"id": 2, "caption": "Метод Виженера", "json_params": {"text": "str", "key": "str"},
     "description": "Метод полиалфавитного шифрования с использованием ключевого слова"},
]

sessions = [
    {"id": 1, "user_id": 1, "method_id": 1, "data_in": "ПРИВЕТ", "params": {"text": "ПРИВЕТ", "shifts": 3},
     "data_out": "МНЁ9ВП", "status": 200, "created_at": "2024-06-16 15:34:12.345678", "time_op": 0.21},
    {"id": 2, "user_id": 2, "method_id": 1, "data_in": "ЁЛКА И ЛАМПОЧКА",
     "params": {"text": "ЁЛКА И ЛАМПОЧКА", "shifts": 1337}, "data_out": "5БА-Х8ХБ-ВЕДМА-", "status": 200,
     "created_at": "2024-06-16 16:54:17.123678", "time_op": 0.27},
    {"id": 3, "user_id": 3, "method_id": 2, "data_in": "КАРЛ УКРАЛ КАРАЛЫ",
     "params": {"text": "КАРЛ УКРАЛ КАРАЛЫ", "keyword": "КЛАР"}, "data_out": "-Э.6К9ЬБЬ1А5Ь6С6Ё", "status": 200,
     "created_at": "2024-05-23 17:25:14.243865", "time_op": 0.22},
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
        users_without_secret.append(new_user)
    return users_without_secret


@app.get("/get_methods")
def get_methods():
    return methods_of_encryption


def identification_user(login: str, secret: str):
    user = next((u for u in users if u["login"] == login and u["secret"] == secret), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid login or secret")
    return user

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


@app.post("/break")
def hack_text(text_for_hack: str, known_word: str) -> dict:
    known_word = known_word.upper()
    for shift in range(len(ALPHABET)):
        decrypted_text = decrypt_cesar_method(text_for_hack, shift)
        if known_word in decrypted_text:
            return {"method": "cesar", "shift": shift, "decrypted_text": decrypted_text}

    keyword_len_range = range(1, len(text_for_hack) // len(known_word) + 2)

    for keyword_len in keyword_len_range:
        for start_idx in range(len(text_for_hack) - len(known_word) + 1):
            substring = text_for_hack[start_idx:start_idx + len(known_word)]
            candidate_keyword = ''
            for i in range(len(known_word)):
                keyword_char = known_word[i]
                encrypted_char = substring[i]
                encrypted_index = ALPHABET.index(encrypted_char)
                key_char = keyword_char.upper()
                key_index = ALPHABET.index(key_char)
                new_index = (encrypted_index - key_index) % len(ALPHABET)
                candidate_keyword += ALPHABET[new_index]
            decrypted_text = decrypt_vigenere_method(text_for_hack, candidate_keyword)
            if known_word in decrypted_text:
                return {"method": "vigenere", "keyword": candidate_keyword, "decrypted_text": decrypted_text}

    return {"status": 404, "message": "Decryption failed"}


@app.get("/get_session/{session_id}")
def get_session(session_id: int, login: str, secret: str):
    user = identification_user(login, secret)
    session = next((s for s in sessions if s["id"] == session_id and s["user_id"] == user["id"]), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    return session


@app.delete("/delete_session/{session_id}")
def delete_session(session_id: int, login: str, secret: str):
    user = identification_user(login, secret)
    session_index = next((i for i, s in enumerate(sessions) if s["id"] == session_id and s["user_id"] == user["id"]), None)
    if session_index is None:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    del sessions[session_index]
    return {"status": 200, "data": sessions}
