from typing import Tuple, Dict
from ..decorators.validar_request import ValidarRequest
from ..db.database import Usuario
from flask import request
from psycopg2.errors import UniqueViolation
from ..utils.senha import criptografar


class Cadastro:

    @ValidarRequest(
        {
            "nome": {"type": "string", "empty": False, "required": True},
            "email": {"type": "string", "empty": False, "required": True},
            "senha": {"type": "string", "empty": False, "required": True},
            "endereco": {"type": "string", "empty": False, "required": True},
            "numero_endereco": {"type": "string", "empty": False, "required": True},
            "complemento_endereco": {"type": "string", "empty": True, "required": True},
            "cep": {"type": "string", "empty": False, "required": True},
            "data_nascimento": {"type": "string", "empty": False, "required": True},
        }
    )
    def post(self, db_session) -> Tuple[str, int]:
        request_json: Dict[str, str] = request.get_json()
        usuario: Usuario = Usuario(
            request_json["nome"],
            request_json["email"],
            criptografar(request_json["senha"]),
            request_json["endereco"],
            request_json["numero_endereco"],
            request_json["complemento_endereco"],
            request_json["cep"],
            request_json["data_nascimento"],
            0
        )
        try:
            db_session.add(usuario)
            db_session.commit()
            return "criado", 201
        except Exception as e:
            if isinstance(e.orig, UniqueViolation):
                return "email ja cadastrado", 409
            return "ocorreu um erro desconhecido", 520
