from typing import Tuple, List, Dict
from flask import request
from ..db.database import db_session
from ..db.database import Denuncia as DenunciaEntity
from ..db.database import Usuario as UsuarioEntity
from psycopg2.errors import (
    InvalidTextRepresentation,
    ForeignKeyViolation,
)
from ..utils.azure import upload_blob
from uuid import uuid4
from datetime import datetime, timedelta
from os import getenv
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, or_
from geoalchemy2 import Geography
from sqlalchemy.sql.expression import cast
from ..db.database import Categoria
import traceback


class Denuncia:

    def post(self) -> Tuple[Dict[str, str], int]:
        try:
            fotos: List[Dict[str, str]] = [
                {"nome": f"imagem_{uuid4()}.jpg", "base64": foto}
                for foto in request.json.get("fotos")
            ]
            data = datetime.strptime(request.json.get("data"), "%Y-%m-%d %H:%M:%S.%f")
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
                "|".join(
                    [
                        f"{getenv('AZURE_BLOB_URL')}/{getenv('AZURE_BLOB_CONTAINER_DENUNCIAS')}/{foto['nome']}"
                        for foto in fotos
                    ]
                ),
                0,
                request.token_id,
                "nao_resolvido",
                None,
                func.ST_SetSRID(
                    func.ST_MakePoint(
                        request.json.get("longitude"), request.json.get("latitude")
                    ),
                    4326,
                ),
            )
            db_session.add(denuncia)
            db_session.flush()
            for foto in fotos:
                upload_blob(
                    foto["base64"],
                    foto["nome"],
                    getenv("AZURE_BLOB_CONTAINER_DENUNCIAS"),
                )
            db_session.commit()
            return {"msg": "criado"}, 201
        except ValueError:
            return {"msg": "data invalida"}, 409
        except Exception as e:
            db_session.rollback()
            if isinstance(e.orig, InvalidTextRepresentation):
                return {"msg": "categoria invalida"}, 409
            if isinstance(e.orig, ForeignKeyViolation):
                return {"msg": "usuario inexistente"}, 409
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def get(self) -> Tuple[List[Dict[str, str]], int]:
        try:
            if request.args.get("id"):
                denuncia = (
                    db_session.query(DenunciaEntity)
                    .filter(
                        DenunciaEntity.id == request.args.get("id"),
                        DenunciaEntity.delete == False,
                    )
                    .one()
                )
                return self.denuncia_json(denuncia), 200
            if (
                request.args.get("latitude")
                and request.args.get("longitude")
                and request.args.get("page") != None
            ):
                LIMIT: int = 10
                page: int = int(request.args.get("page"))
                query = db_session.query(
                    DenunciaEntity.status,
                    DenunciaEntity.id,
                    DenunciaEntity.descricao,
                    DenunciaEntity.fotos,
                    DenunciaEntity.endereco,
                    DenunciaEntity.numero_endereco,
                    DenunciaEntity.categoria,
                    UsuarioEntity.nome,
                    UsuarioEntity.foto,
                ).join(UsuarioEntity, DenunciaEntity.usuario_id == UsuarioEntity.id)
                if v := request.args.get("categoria"):
                    if v not in [i for i in Categoria.__dict__.keys() if i[:1] != "_"]:
                        return {"msg": "categoria invalida"}, 409
                    query = query.filter(
                        DenunciaEntity.categoria == v,
                    )
                query = query.filter(
                    DenunciaEntity.delete == False,
                    or_(
                        DenunciaEntity.atualizacao_status
                        > (datetime.now() - timedelta(weeks=1)).strftime(
                            "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        DenunciaEntity.status == "nao_resolvido",
                    ),
                )
                denuncias = (
                    query.order_by(
                        func.ST_Distance(
                            DenunciaEntity.geom,
                            cast(
                                func.ST_MakePoint(
                                    float(request.args.get("longitude")),
                                    float(request.args.get("latitude")),
                                ),
                                Geography,
                            ),
                        ),
                        DenunciaEntity.qtd_curtidas.desc(),
                        DenunciaEntity.criacao.desc(),
                    )
                    .offset(page * LIMIT)
                    .limit(LIMIT)
                    .all()
                )
                return [
                    self.denuncia_json_feed(denuncia, page) for denuncia in denuncias
                ], 200
            return {"msg": "parametros invalidos"}, 409
        except NoResultFound:
            return {"msg": "denuncia nao encontrada"}, 404
        except:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def put(self) -> Tuple[Dict[str, str], int]:
        try:
            request_json = request.get_json()
            denuncia = (
                db_session.query(DenunciaEntity)
                .filter(
                    DenunciaEntity.id == request.args.get("id"),
                    DenunciaEntity.delete == False,
                    DenunciaEntity.usuario_id == request.token_id,
                )
                .one()
            )
            if not request.json:
                return {"msg": "nada foi alterado"}, 200
            if v := request_json.get("descricao"):
                denuncia.descricao = v
            if v := request_json.get("data"):
                denuncia.data = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
            if v := request_json.get("categoria"):
                denuncia.categoria = v
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
            if request_json.get("longitude") or request_json.get("latitude"):
                denuncia.geom = func.ST_SetSRID(
                    func.ST_MakePoint(
                        request_json.get("longitude"), request_json.get("latitude")
                    ),
                    4326,
                )
            if v := request_json.get("status"):
                denuncia.status = v
                denuncia.atualizacao_status = datetime.now()
            db_session.add(denuncia)
            db_session.commit()
            return self.denuncia_json(denuncia), 200
        except NoResultFound:
            return {"msg": "denuncia nao encontrada"}, 404
        except:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

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
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def minhas_denuncias(self) -> Tuple[List[Dict[str, str]], int]:
        try:
            LIMIT: int = 10
            page: int = int(request.args.get("page"))
            query = db_session.query(
                DenunciaEntity.status,
                DenunciaEntity.id,
                DenunciaEntity.descricao,
                DenunciaEntity.fotos,
                DenunciaEntity.endereco,
                DenunciaEntity.numero_endereco,
                DenunciaEntity.categoria,
                UsuarioEntity.nome,
                UsuarioEntity.foto,
            ).join(UsuarioEntity, DenunciaEntity.usuario_id == UsuarioEntity.id)
            if v := request.args.get("categoria"):
                if v not in [i for i in Categoria.__dict__.keys() if i[:1] != "_"]:
                    return {"msg": "categoria invalida"}, 409
                query = query.filter(
                    DenunciaEntity.categoria == v,
                    DenunciaEntity.usuario_id == request.token_id,
                    DenunciaEntity.delete == False,
                )
            else:
                query = query.filter(
                    DenunciaEntity.usuario_id == request.token_id,
                    DenunciaEntity.delete == False,
                )
            denuncias = (
                query.order_by(
                    DenunciaEntity.criacao.desc(),
                )
                .offset(page * LIMIT)
                .limit(LIMIT)
                .all()
            )
            return [
                self.denuncia_json_feed(denuncia, page) for denuncia in denuncias
            ], 200
        except:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

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
            "fotos": denuncia.fotos.split("|"),
            "qtd_curtidas": denuncia.qtd_curtidas,
            "status": denuncia.status.value,
        }

    def denuncia_json_feed(self, denuncia, page: int) -> Dict[str, str]:
        return {
            "status": denuncia.status.value,
            "id": denuncia.id,
            "descricao": denuncia.descricao,
            "fotos": denuncia.fotos.split("|"),
            "endereco": denuncia.endereco,
            "numero_endereco": denuncia.numero_endereco,
            "categoria": denuncia.categoria.value,
            "nome_usuario": denuncia.nome,
            "foto_usuario": denuncia.foto,
            "page": page,
        }
