from typing import Dict
import jwt
from os import getenv


def gerar(payload: Dict[str, any]) -> str:
    key = getenv("JWT_KEY")
    token = jwt.encode(payload, key, "HS256")
    return token
