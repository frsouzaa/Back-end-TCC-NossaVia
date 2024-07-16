from typing import Tuple, Dict
from ..decorators.validar_request import ValidarRequest


class Login():

    @ValidarRequest({
        'email': {'type': 'string', 'empty': False, 'required': True},
        'senha': {'type': 'string', 'empty': False, 'required': True},
    })
    def post(self) -> Tuple[Dict[str, str], int]:
        return "é no detalhe que o diabo se esconde, matue", 666
