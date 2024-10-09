from flask.views import View as FlaskView
from flask import Response, request
from typing import List, Tuple, Dict
from ..controller.denuncia import Denuncia as DenunciaController
from ..decorators.validar_token import ValidarToken
from ..decorators.validar_request import ValidarRequest


class Denuncia(FlaskView):
    rota: str = "/denuncia"
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
            "descricao": {"type": "string", "empty": False, "required": True},
            "categoria": {"type": "string", "empty": False, "required": True},
            "data": {"type": "string", "empty": False, "required": True},
            "endereco": {
                "type": "string",
                "empty": False,
                "required": False,
            },
            "numero_endereco": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "ponto_referencia": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "cep": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "latitude": {"type": "string", "empty": False, "required": True},
            "longitude": {"type": "string", "empty": False, "required": True},
            "fotos": {
                "type": "list",
                "schema": {"type": "string"},
                "empty": False,
                "required": True,
            },
        }
    )
    @ValidarToken()
    def post(self) -> Tuple[Dict[str, str], int]:
        return DenunciaController().post()

    @ValidarRequest(
        args={
            "id": {"type": "string", "empty": False, "required": False},
            "latitude": {"type": "string", "empty": True, "required": False},
            "longitude": {"type": "string", "empty": True, "required": False},
            "page": {"type": "string", "empty": False, "required": False},
            "categoria": {"type": "string", "empty": False, "required": False},
        }
    )
    def get(self) -> Tuple[Dict[str, str], int]:
        return DenunciaController().get()

    @ValidarRequest(
        {
            "descricao": {"type": "string", "empty": False, "required": False},
            "data": {"type": "string", "empty": False, "required": False},
            "categoria": {"type": "string", "empty": False, "required": False},
            "endereco": {
                "type": "string",
                "empty": False,
                "required": False,
            },
            "numero_endereco": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "ponto_referencia": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "cep": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "latitude": {"type": "string", "empty": False, "required": False},
            "longitude": {"type": "string", "empty": False, "required": False},
            "status": {"type": "string", "empty": False, "required": False},
        },
        args={
            "id": {"type": "string", "empty": False, "required": True},
        },
    )
    @ValidarToken()
    def put(self) -> Tuple[Dict[str, str], int]:
        return DenunciaController().put()

    @ValidarRequest(
        args={
            "id": {"type": "string", "empty": False, "required": True},
        }
    )
    @ValidarToken()
    def delete(self) -> Tuple[Dict[str, str], int]:
        return DenunciaController().delete()
