from typing import Callable, Dict, Tuple
from flask import request
from cerberus import Validator


class ValidarRequest:
    req: Dict[str, any]
    validate: str

    def __init__(self, req: Dict[str, any] = None, validate: str = "json") -> None:
        self.req = req
        self.validate = validate

    def __call__(
            self, func: Callable) -> Tuple[Dict[str, str], int] | Callable:
        def valida_request(f=None, *args, **kwargs):
            v = Validator(self.req)
            if (self.validate == "json" and v.validate(request.get_json()) is not True):
                return {"msg": v.errors}, 400
            elif (self.validate == "args" and v.validate(request.args) is not True):
                return {"msg": v.errors}, 400
            if f is not None:
                return func(f, *args, **kwargs)
            return func(*args, **kwargs)
        return valida_request
