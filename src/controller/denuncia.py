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
            "nao_resolvido",
            None,
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
        request_json = request.get_json()
        try:
            if not request.json:
                return {"msg": "nada foi alterado"}, 200
            denuncia = (
                db_session.query(DenunciaEntity)
                .filter(
                    DenunciaEntity.id == request.args.get("id"),
                    DenunciaEntity.delete == False,
                    DenunciaEntity.usuario_id == request.token_id,
                )
                .one()
            )
            if v := request_json.get("descricao"):
                denuncia.descricao = v
            if v := request_json.get("data"):
                denuncia.data = datetime.strptime(
                    v, "%Y-%m-%d %H:%M:%S.%f"
                )
            if v := request_json.get("endereco"):
                denuncia.endereco = v
            if v := request_json.get("numero_endereco"):
                denuncia.numero_endereco = v
            if v := request_json.get("ponto_referencia"):
                denuncia.ponto_referencia = v
            if v := request_json.get("cep"):
                denuncia.cep = v
            if v := request_json.get("latitude"):
                denuncia.latitude = v
            if v := request_json.get("longitude"):
                denuncia.longitude = v
            if v := request_json.get("status"):
                denuncia.status = v
                denuncia.atualizacao_status = datetime.now()
            db_session.add(denuncia)
            db_session.commit()
            return self.denuncia_json(denuncia), 200
        except NoResultFound:
            return {"msg": "denuncia nao encontrada"}, 404
        except:
            return {"msg": "ocorreu um erro desconhecido"}, 520

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

    def denuncia_json(self, denuncia: DenunciaEntity) -> Dict[str, str]:
        return {
            "id": denuncia.id,
            "criacao": denuncia.criacao,
            "descricao": denuncia.descricao,
            "categoria": denuncia.categoria.value,
            "data": denuncia.data,
            "endereco": denuncia.endereco,
            "numero_endereco": denuncia.numero_endereco,
            "ponto_referencia": denuncia.ponto_referencia,
            "cep": denuncia.cep,
            "latitude": denuncia.latitude,
            "longitude": denuncia.longitude,
            "fotos": denuncia.fotos,
            "qtd_curtidas": denuncia.qtd_curtidas,
            "status": denuncia.status.value,
        }
