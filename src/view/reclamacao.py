from flask.views import View as FlaskView
from flask import Response, request
from typing import List, Tuple, Dict
from ..controller.reclamacao import Reclamacao as ReclamacaoController
from ..decorators.validar_token import ValidarToken
from ..decorators.validar_request import ValidarRequest


class Reclamacao(FlaskView):
    rota: str = "/reclamacao"
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
            "cep": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "endereco": {
                "type": "string",
                "empty": False,
                "required": True,
            },
            "numero_endereco": {
                "type": "string",
                "empty": False,
                "required": True,
            },
            "ponto_referencia": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "bairro": {
                "type": "string",
                "empty": False,
                "required": True,
            },
            "cidade": {
                "type": "string",
                "empty": False,
                "required": True,
            },
            "estado": {
                "type": "string",
                "empty": False,
                "required": True,
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
        return ReclamacaoController().post()

    @ValidarRequest(
        args={
            "id": {"type": "string", "empty": False, "required": False},
            "latitude": {"type": "string", "empty": True, "required": False},
            "longitude": {"type": "string", "empty": True, "required": False},
            "page": {"type": "string", "empty": False, "required": False},
            "categoria": {"type": "string", "empty": False, "required": False},
        }
    )
    @ValidarToken(True)
    def get(self) -> Tuple[Dict[str, str], int]:
        return ReclamacaoController().get()

    @ValidarRequest(
        {
            "descricao": {"type": "string", "empty": False, "required": False},
            "data": {"type": "string", "empty": False, "required": False},
            "categoria": {"type": "string", "empty": False, "required": False},
            "cep": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": True,
            },
            "endereco": {
                "type": "string",
                "empty": False,
                "required": False,
            },
            "numero_endereco": {
                "type": "string",
                "empty": False,
                "required": False,
            },
            "ponto_referencia": {
                "type": "string",
                "empty": True,
                "required": False,
                "nullable": False,
            },
            "bairro": {
                "type": "string",
                "empty": False,
                "required": False,
            },
            "cidade": {
                "type": "string",
                "empty": False,
                "required": False,
            },
            "estado": {
                "type": "string",
                "empty": False,
                "required": False,
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
        return ReclamacaoController().put()

    @ValidarRequest(
        args={
            "id": {"type": "string", "empty": False, "required": True},
        }
    )
    @ValidarToken()
    def delete(self) -> Tuple[Dict[str, str], int]:
        return ReclamacaoController().delete()
