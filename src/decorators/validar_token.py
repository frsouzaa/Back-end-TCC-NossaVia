import jwt
from flask import request
from typing import Callable, Tuple
from os import getenv


class ValidarToken:

    def __call__(self, func: Callable) -> Tuple[str, int] | Callable:
        def valida_token(f=None, *args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                return "Está faltando o token", 401
            try:
                jwt.decode(token, getenv("JWT_KEY"), algorithms=["HS256"])
            except:
                return "Token inválido", 401
            if f is not None:
                return func(f, *args, **kwargs)
            return func(*args, **kwargs)
        return valida_token
