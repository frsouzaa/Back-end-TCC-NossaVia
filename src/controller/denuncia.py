from typing import Tuple, Dict
from ..decorators.validar_token import ValidarToken
from ..db.database import Usuario
from flask import jsonify, request
from ..utils.senha import descriptografar
from ..utils.jwt import gerar as gerar_jwt
from ..db.database import db_session


class Denuncia:

    @ValidarToken()
    def post(self) -> Tuple[Dict[str, str] | str, int]:
        return "criado", 201
