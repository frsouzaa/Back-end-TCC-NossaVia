from typing import Tuple, Dict
from ..decorators.validar_request import ValidarRequest
from ..db.database import Usuario
from flask import jsonify, request


class Login:

    @ValidarRequest(
        {
            "email": {"type": "string", "empty": False, "required": True},
            "senha": {"type": "string", "empty": False, "required": True},
        }
    )
    def post(self) -> Tuple[Dict[str, str], int]:
        request_json = request.get_json()
        res = Usuario.query.filter(
            Usuario.email == request_json["email"],
            Usuario.senha == request_json["senha"],
        ).one()
        return jsonify(res), 200
