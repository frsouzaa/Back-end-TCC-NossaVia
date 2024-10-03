from typing import Tuple, List, Dict
from flask import request
from ..db.database import db_session
from ..db.database import Denuncia as DenunciaEntity
from psycopg2.errors import (
    InvalidTextRepresentation,
    ForeignKeyViolation,
)
from ..utils.azure import upload_blob
from uuid import uuid4
from datetime import datetime
from os import getenv
from sqlalchemy.orm.exc import NoResultFound


class Denuncia:

    def post(self) -> Tuple[Dict[str, str], int]:
        fotos: List[Dict[str, str]] = [
            {"nome": f"imagem_{uuid4()}.jpg", "base64": foto}
            for foto in request.json.get("fotos")
        ]
        try:
            data = datetime.strptime(request.json.get("data"), "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            return {"msg": "data invalida"}, 409
        denuncia: DenunciaEntity = DenunciaEntity(
            request.json.get("descricao"),
            request.json.get("categoria"),
            data,
            request.json.get("endereco"),
            request.json.get("numero_endereco"),
            request.json.get("ponto_referencia"),
            request.json.get("cep"),
            request.json.get("latitude"),
            request.json.get("longitude"),
            [
                f"{getenv('AZURE_BLOB_URL')}/{getenv('AZURE_BLOB_CONTAINER_DENUNCIAS')}/{foto['nome']}"
                for foto in fotos
            ],
            0,
            request.token_id,
        )
        try:
            db_session.add(denuncia)
            db_session.flush()
            for foto in fotos:
                upload_blob(
                    foto["base64"],
                    foto["nome"],
                    getenv("AZURE_BLOB_CONTAINER_DENUNCIAS"),
                )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            if isinstance(e.orig, InvalidTextRepresentation):
                return {"msg": "categoria invalida"}, 409
            if isinstance(e.orig, ForeignKeyViolation):
                return {"msg": "usuario inexistente"}, 409
            return {"msg": "ocorreu um erro desconhecido"}, 520
        return {"msg": "criado"}, 201

    def get(self) -> Tuple[List[Dict[str, str]], int]:
        return "TODO", 501

    def put(self) -> Tuple[Dict[str, str], int]:
        return "TODO", 501

    def delete(self) -> Tuple[Dict[str, str], int]:
        try:
            denuncia = (
                db_session.query(DenunciaEntity)
                .filter(
                    DenunciaEntity.id == request.args.get("id"),
                    DenunciaEntity.delete == False,
                    DenunciaEntity.usuario_id == request.token_id,
                )
                .one()
            )
            denuncia.delete = True
            denuncia.modificacao = datetime.now()
            db_session.add(denuncia)
            db_session.commit()
            return {"msg": "deletado"}, 200
        except NoResultFound:
            return {"msg": "denuncia nao encontrada"}, 404
        except:
            return {"msg": "ocorreu um erro desconhecido"}, 520
