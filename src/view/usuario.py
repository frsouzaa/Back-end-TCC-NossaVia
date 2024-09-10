from flask.views import View as FlaskView
from flask import Response
from typing import List, Tuple, Dict
from ..controller.usuario import Usuario as UsuarioController
from flask import request
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
            if not request.args.get("id"):
                return "id nao informado", 400
            return self.get(request.args.get("id"))
        if request.method == "PUT":
            if not request.args.get("id"):
                return "id nao informado", 400
            return self.put(request.args.get("id"))
        if request.method == "DELETE":
            if not request.args.get("id"):
                return "id nao informado", 400
            return self.delete(request.args.get("id"))

    @ValidarRequest(
        {
            "nome": {"type": "string", "empty": False, "required": True},
            "email": {"type": "string", "empty": False, "required": True},
            "senha": {"type": "string", "empty": False, "required": True},
            "endereco": {"type": "string", "empty": False, "required": True},
            "numero_endereco": {"type": "string", "empty": True, "required": False},
            "complemento_endereco": {"type": "string", "empty": True, "required": False},
            "cep": {"type": "string", "empty": False, "required": True},
            "data_nascimento": {"type": "string", "empty": False, "required": True},
            "sexo": {"type": "string", "empty": False, "required": True},
            "telefone": {"type": "string", "empty": False, "required": True},
        }
    )
    def post(self) -> Tuple[Dict[str, str], int]:
        return UsuarioController().post()

    @ValidarToken()
    def get(self, id: int) -> Tuple[Dict[str, str], int]:
        return UsuarioController().get(id)

    @ValidarRequest(
        {
            "nome": {"type": "string", "empty": False, "required": False},
            "senha": {"type": "string", "empty": False, "required": False},
            "endereco": {"type": "string", "empty": False, "required": False},
            "numero_endereco": {"type": "string", "empty": True, "required": False},
            "complemento_endereco": {"type": "string", "empty": True, "required": False},
            "cep": {"type": "string", "empty": False, "required": False},
            "data_nascimento": {"type": "string", "empty": False, "required": False},
            "sexo": {"type": "string", "empty": False, "required": False},
            "telefone": {"type": "string", "empty": False, "required": False},
        }
    )
    @ValidarToken()
    def put(self, id: int) -> Tuple[Dict[str, str], int]:
        return UsuarioController().put(id)
    
    @ValidarToken()
    def delete(self, id: int) -> Tuple[Dict[str, str], int]:
        return UsuarioController().delete(id)