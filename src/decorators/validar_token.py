import jwt
from flask import request
from typing import Callable, Tuple
from os import getenv


class ValidarToken:
    continue_on_empty: bool

    def __init__(self, continue_on_empty=False) -> None:
        self.continue_on_empty = continue_on_empty

    def __call__(self, func: Callable) -> Tuple[str, int] | Callable:
        def valida_token(f=None, *args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                if self.continue_on_empty:
                    if f is not None:
                        return func(f, *args, **kwargs)
                    return func(*args, **kwargs)
                return {"msg": "Está faltando o token"}, 401
            try:
                request.token_id = jwt.decode(
                    token, getenv("JWT_KEY"), algorithms=["HS256"]
                )["id"]
            except BaseException:
                return {"msg": "Token inválido"}, 401
            if f is not None:
                return func(f, *args, **kwargs)
            return func(*args, **kwargs)

        return valida_token
