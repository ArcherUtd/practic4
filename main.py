from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

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
    {"login": "VinnikovSolaris", "secret": "WestGym"},
    {"login": "MironAlkash", "secret": "Chery Tiggo 4 Pro Max"},

]


methods_of_encryption=[
    {"id": 1, "caption": "Метод Цезаря", "json_params": {"text": "str", "shifts": "int"}, "description": "Шифруется методом сдвига"},
    {"id": 2, "caption": "Метод Виженера", "json_params": {"text": "str", "key": "str"}, "description": "Метод полиалфавитного шифрования с использованием ключевого слова"},
]


@app.post("/user")
def append_user(user: List[User]):
    users.extend(user)
    return users


