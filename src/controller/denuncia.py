from typing import Tuple, List, Dict
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

    def post(self) -> Tuple[str, int]:
        fotos: List[Dict[str, str]] = [
            {"nome": f"imagem_{uuid4()}.jpg", "base64": foto}
            for foto in request.json.get("fotos")
        ]
        denuncia: DenunciaEntity = DenunciaEntity(
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
            request.token_id,
        )
        try:
            for foto in fotos:
                upload_blob(foto["base64"], foto["nome"])
        except Exception as e:
            return {"msg": "ocorreu um erro desconhecido"}, 520
        try:
            db_session.add(denuncia)
            db_session.commit()
        except Exception as e:
            if isinstance(e.orig, InvalidTextRepresentation):
                return {"msg": "categoria invalida"}, 409
            if isinstance(e.orig, InvalidDatetimeFormat):
                return {"msg": "data invalida"}, 409
            if isinstance(e.orig, ForeignKeyViolation):
                return {"msg": "usuario inexistente"}, 409
            return {"msg": "ocorreu um erro desconhecido"}, 520
        return {"msg": "criado"}, 201
