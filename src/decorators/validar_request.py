from typing import Callable, Dict, Tuple
from flask import request
from cerberus import Validator


class ValidarRequest:
    json: Dict[str, any]
    args: Dict[str, any]

    def __init__(
        self, json: Dict[str, any] = None, args: Dict[str, any] = None
    ) -> None:
        self.json = json
        self.args = args

    def __call__(self, func: Callable) -> Tuple[Dict[str, str], int] | Callable:
        def valida_request(f=None, *args, **kwargs):
            if self.json:
                v = Validator(self.json)
                if v.validate(request.get_json()) is not True:
                    return {"msg": v.errors}, 400
            if self.args:
                v = Validator(self.args)
                if v.validate(request.args) is not True:
                    return {"msg": v.errors}, 400
            if f is not None:
                return func(f, *args, **kwargs)
            return func(*args, **kwargs)

        return valida_request
