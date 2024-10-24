from flask.views import View as FlaskView
from flask import Response
from typing import List, Tuple, Dict
from ..controller.recuperar_senha import RecuperarSenha as RecuperarSenhaController
from ..decorators.validar_request import ValidarRequest
from flask import request


class RecuperarSenha(FlaskView):
    rota: str = "/recuperar-senha"
    methods: List[str] = ["post", "get", "put"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        if request.method == "POST":
            return self.post()
        if request.method == "GET":
            return self.get()
        if request.method == "PUT":
            return self.put()

    @ValidarRequest(
        {
            "email": {"type": "string", "empty": False, "required": True},
        }
    )
    def post(self) -> Tuple[Dict[str, str], int]:
        return RecuperarSenhaController().post()
    
    @ValidarRequest(
        args = {
            "email": {"type": "string", "empty": False, "required": True},
            "token": {"type": "string", "empty": False, "required": True},
        }
    )
    def get(self) -> Tuple[Dict[str, str], int]:
        return RecuperarSenhaController().get()

    @ValidarRequest(
        {
            "email": {"type": "string", "empty": False, "required": True},
            "token": {"type": "string", "empty": False, "required": True},
            "senhaNova": {"type": "string", "empty": False, "required": True},
        }
    )
    def put(self) -> Tuple[Dict[str, str], int]:
        return RecuperarSenhaController().put()
