from flask.views import View as FlaskView
from flask import Response, request
from typing import List, Tuple, Dict
from ..controller.usuario import Usuario as UsuarioController
from ..decorators.validar_token import ValidarToken
from ..decorators.validar_request import ValidarRequest


class Usuario(FlaskView):
    rota: str = "/usuario"
    methods: List[str] = ["post", "get", "put", "delete"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        if request.method == "POST":
            return self.post()
        if request.method == "GET":
            return self.get()
        if request.method == "PUT":
            return self.put()
        if request.method == "DELETE":
            return self.delete()

    @ValidarRequest(
        {
            "nome": {"type": "string", "empty": False, "required": True},
            "email": {"type": "string", "empty": False, "required": True},
            "senha": {"type": "string", "empty": False, "required": True},
            "endereco": {"type": "string", "empty": False, "required": True},
            "numero_endereco": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "complemento_endereco": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "cep": {"type": "string", "empty": False, "required": True},
            "data_nascimento": {"type": "string", "empty": False, "required": True},
            "sexo": {"type": "string", "empty": False, "required": True},
            "telefone": {"type": "string", "empty": False, "required": True},
        }
    )
    def post(self) -> Tuple[Dict[str, str], int]:
        return UsuarioController().post()

    @ValidarToken()
    def get(self) -> Tuple[Dict[str, str], int]:
        return UsuarioController().get()

    @ValidarRequest(
        {
            "nome": {"type": "string", "empty": False, "required": False},
            "endereco": {"type": "string", "empty": False, "required": False},
            "numero_endereco": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "complemento_endereco": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "cep": {"type": "string", "empty": False, "required": False},
            "data_nascimento": {"type": "string", "empty": False, "required": False},
            "sexo": {"type": "string", "empty": False, "required": False},
            "telefone": {"type": "string", "empty": False, "required": False},
            "foto": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
        }
    )
    @ValidarToken()
    def put(self) -> Tuple[Dict[str, str], int]:
        return UsuarioController().put()

    @ValidarToken()
    def delete(self) -> Tuple[Dict[str, str], int]:
        return UsuarioController().delete()
