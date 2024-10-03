from typing import Tuple, Dict
from ..db.database import Usuario
from flask import request
from ..utils.senha import descriptografar, criptografar
from ..db.database import db_session
from datetime import datetime


class AlterarSenha:

    def post(self) -> Tuple[Dict[str, str] | str, int]:
        request_json: Dict[str, str] = request.get_json()
        usuario = Usuario.query.filter(
            Usuario.id == request.token_id, Usuario.delete == False
        ).one()
        if not usuario or not descriptografar(
            request_json["senhaAtual"], usuario.senha
        ):
            return {"msg": "senha atual incorreta"}, 400
        usuario.senha = criptografar(request_json["senhaNova"])
        usuario.modificacao = datetime.now()
        db_session.add(usuario)
        db_session.commit()
        return {"msg": "senha alterada"}, 200
