from typing import Tuple, Dict
from ..decorators.validar_request import ValidarRequest
from ..db.database import Usuario
from flask import jsonify, request
from ..utils.senha import descriptografar
from ..utils.jwt import gerar as gerar_jwt


class Login:

    @ValidarRequest(
        {
            "email": {"type": "string", "empty": False, "required": True},
            "senha": {"type": "string", "empty": False, "required": True},
        }
    )
    def post(self) -> Tuple[Dict[str, str] | str, int]:
        request_json: Dict[str, str] = request.get_json()
        res = Usuario.query.filter(
            Usuario.email == request_json["email"], Usuario.delete == False
        ).first()
        if not res or not descriptografar(request_json["senha"], res.senha):
            return {"msg": "usuário ou senha incorretos"}, 401
        return jsonify({"token": gerar_jwt({"id": str(res.id)})}), 200
