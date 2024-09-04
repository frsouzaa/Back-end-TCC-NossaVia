from typing import Tuple, List, Dict
from ..decorators.validar_token import ValidarToken
from ..decorators.validar_request import ValidarRequest
from flask import request
from ..db.database import db_session
from ..db.database import Denuncia as DenunciaEntity
from psycopg2.errors import (
    InvalidTextRepresentation,
    InvalidDatetimeFormat,
    ForeignKeyViolation,
)
from ..utils.azure import upload_blob
from uuid import uuid4
from os import getenv


class Denuncia:

    @ValidarRequest(
        {
            "titulo": {"type": "string", "empty": False, "required": True},
            "descricao": {"type": "string", "empty": False, "required": True},
            "categoria": {"type": "string", "empty": False, "required": True},
            "data": {"type": "string", "empty": False, "required": True},
            "endereco": {"type": "string", "empty": False, "required": False},
            "numero_endereco": {"type": "string", "empty": False, "required": False},
            "ponto_referencia": {"type": "string", "empty": False, "required": False},
            "cep": {"type": "string", "empty": False, "required": False},
            "latitude": {"type": "string", "empty": False, "required": True},
            "longitude": {"type": "string", "empty": False, "required": True},
            "fotos": {
                "type": "list",
                "schema": {"type": "string"},
                "empty": False,
                "required": True,
            },
            "usuario_id": {"type": "integer", "empty": False, "required": True},
        }
    )
    @ValidarToken()
    def post(self) -> Tuple[str, int]:
        fotos: List[Dict[str, str]] = [
            {"nome": f"imagem_{uuid4()}.jpg", "base64": foto}
            for foto in request.json.get("fotos")
        ]
        denuncia: DenunciaEntity = DenunciaEntity(
            request.json.get("titulo"),
            request.json.get("descricao"),
            request.json.get("categoria"),
            request.json.get("data"),
            request.json.get("endereco"),
            request.json.get("numero_endereco"),
            request.json.get("ponto_referencia"),
            request.json.get("cep"),
            request.json.get("latitude"),
            request.json.get("longitude"),
            [f"{getenv('AZURE_BLOB_URL')}/{foto['nome']}" for foto in fotos],
            0,
            request.json.get("usuario_id"),
        )
        try:
            for foto in fotos:
                upload_blob(foto["base64"], foto["nome"])
        except Exception as e:
            return "ocorreu um erro desconhecido", 520
        try:
            db_session.add(denuncia)
            db_session.commit()
        except Exception as e:
            if isinstance(e.orig, InvalidTextRepresentation):
                return "categoria invalida", 409
            if isinstance(e.orig, InvalidDatetimeFormat):
                return "data invalida", 409
            if isinstance(e.orig, ForeignKeyViolation):
                return "usuario inexistente", 409
            return "ocorreu um erro desconhecido", 520
        return "criado", 201
