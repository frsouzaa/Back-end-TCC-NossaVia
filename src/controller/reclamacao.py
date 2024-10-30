from typing import Tuple, List, Dict
from flask import request
from ..db.database import db_session
from ..db.database import Reclamacao as ReclamacaoEntity
from ..db.database import Usuario as UsuarioEntity
from ..db.database import Curtida as CurtidaEntity
from psycopg2.errors import (
    InvalidTextRepresentation,
    ForeignKeyViolation,
)
from ..utils.azure import upload_blob
from uuid import uuid4
from datetime import datetime, timedelta
from os import getenv
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, or_, and_
from ..db.database import Categoria
import traceback


class Reclamacao:

    def post(self) -> Tuple[Dict[str, str], int]:
        try:
            fotos: List[Dict[str, str]] = [
                {"nome": f"imagem_{uuid4()}.jpg", "base64": foto}
                for foto in request.json.get("fotos")
            ]
            data = datetime.strptime(request.json.get("data"), "%Y-%m-%d %H:%M:%S.%f")
            reclamacao: ReclamacaoEntity = ReclamacaoEntity(
                request.json.get("descricao"),
                request.json.get("categoria"),
                data,
                request.json.get("cep"),
                request.json.get("endereco"),
                request.json.get("numero_endereco"),
                request.json.get("ponto_referencia"),
                request.json.get("bairro"),
                request.json.get("cidade"),
                request.json.get("estado"),
                request.json.get("latitude"),
                request.json.get("longitude"),
                "|".join(
                    [
                        f"{getenv('AZURE_BLOB_URL')}/{getenv('AZURE_BLOB_CONTAINER_RECLAMACOES')}/{foto['nome']}"
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
            db_session.add(reclamacao)
            db_session.flush()
            for foto in fotos:
                upload_blob(
                    foto["base64"],
                    foto["nome"],
                    getenv("AZURE_BLOB_CONTAINER_RECLAMACOES"),
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
                if hasattr(request, "token_id"):
                    reclamacao = (
                        db_session.query(ReclamacaoEntity, UsuarioEntity, CurtidaEntity.delete)
                        .join(
                            UsuarioEntity,
                            ReclamacaoEntity.usuario_id == UsuarioEntity.id,
                        )
                        .join(
                            CurtidaEntity,
                            and_(
                                CurtidaEntity.usuario_id == request.token_id,
                                CurtidaEntity.reclamacao_id == ReclamacaoEntity.id,
                            ),
                            isouter=True,
                        )
                    )
                else:
                    reclamacao = db_session.query(ReclamacaoEntity, UsuarioEntity).join(
                        UsuarioEntity,
                        ReclamacaoEntity.usuario_id == UsuarioEntity.id,
                    )
                reclamacao = reclamacao.filter(
                    ReclamacaoEntity.id == request.args.get("id"),
                    ReclamacaoEntity.delete == False,
                ).one()
                if hasattr(request, "token_id"):
                    return self.reclamacao_json(reclamacao[0], reclamacao[1], reclamacao[2]), 200
                return self.reclamacao_json(reclamacao[0], reclamacao[1], None), 200
            if (
                request.args.get("latitude")
                and request.args.get("longitude")
                and request.args.get("page") != None
            ):
                LIMIT: int = 10
                page: int = int(request.args.get("page"))
                if hasattr(request, "token_id"):
                    query = (
                        db_session.query(
                            ReclamacaoEntity.status,
                            ReclamacaoEntity.id,
                            ReclamacaoEntity.descricao,
                            ReclamacaoEntity.fotos,
                            ReclamacaoEntity.endereco,
                            ReclamacaoEntity.numero_endereco,
                            ReclamacaoEntity.categoria,
                            ReclamacaoEntity.qtd_curtidas,
                            UsuarioEntity.nome,
                            UsuarioEntity.foto,
                            CurtidaEntity.delete.label("curtida"),
                        )
                        .join(
                            UsuarioEntity,
                            ReclamacaoEntity.usuario_id == UsuarioEntity.id,
                        )
                        .join(
                            CurtidaEntity,
                            and_(
                                CurtidaEntity.usuario_id == request.token_id,
                                CurtidaEntity.reclamacao_id == ReclamacaoEntity.id,
                            ),
                            isouter=True,
                        )
                    )
                else:
                    query = db_session.query(
                        ReclamacaoEntity.status,
                        ReclamacaoEntity.id,
                        ReclamacaoEntity.descricao,
                        ReclamacaoEntity.fotos,
                        ReclamacaoEntity.endereco,
                        ReclamacaoEntity.numero_endereco,
                        ReclamacaoEntity.categoria,
                        ReclamacaoEntity.qtd_curtidas,
                        UsuarioEntity.nome,
                        UsuarioEntity.foto,
                    ).join(
                        UsuarioEntity,
                        ReclamacaoEntity.usuario_id == UsuarioEntity.id,
                    )
                if v := request.args.get("categoria"):
                    if v not in [i for i in Categoria.__dict__.keys() if i[:1] != "_"]:
                        return {"msg": "categoria invalida"}, 409
                    query = query.filter(
                        ReclamacaoEntity.categoria == v,
                    )
                query = query.filter(
                    ReclamacaoEntity.delete == False,
                    or_(
                        ReclamacaoEntity.atualizacao_status
                        > (datetime.now() - timedelta(weeks=1)).strftime(
                            "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        ReclamacaoEntity.status == "nao_resolvido",
                    ),
                )
                reclamacoes = (
                    query.order_by(
                        func.ST_Distance(
                            ReclamacaoEntity.geog,
                            func.ST_MakePoint(
                                float(request.args.get("longitude")),
                                float(request.args.get("latitude")),
                            ),
                        ),
                        ReclamacaoEntity.qtd_curtidas.desc(),
                        ReclamacaoEntity.criacao.desc(),
                    )
                    .offset(page * LIMIT)
                    .limit(LIMIT)
                    .all()
                )
                if hasattr(request, "token_id"):
                    return [
                        self.reclamacao_json_feed(reclamacao, page)
                        for reclamacao in reclamacoes
                    ], 200
                return [
                    self.reclamacao_json_feed_pessoal(reclamacao, page)
                    for reclamacao in reclamacoes
                ], 200
            return {"msg": "parametros invalidos"}, 409
        except NoResultFound:
            return {"msg": "reclamacao nao encontrada"}, 404
        except:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def put(self) -> Tuple[Dict[str, str], int]:
        try:
            request_json = request.get_json()
            reclamacao = (
                db_session.query(ReclamacaoEntity)
                .filter(
                    ReclamacaoEntity.id == request.args.get("id"),
                    ReclamacaoEntity.delete == False,
                    ReclamacaoEntity.usuario_id == request.token_id,
                )
                .one()
            )
            if not request.json:
                return {"msg": "nada foi alterado"}, 200
            if v := request_json.get("descricao"):
                reclamacao.descricao = v
            if v := request_json.get("data"):
                reclamacao.data = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
            if v := request_json.get("categoria"):
                reclamacao.categoria = v
            if v := request_json.get("cep"):
                reclamacao.cep = v
            if v := request_json.get("endereco"):
                reclamacao.endereco = v
            if v := request_json.get("numero_endereco"):
                reclamacao.numero_endereco = v
            if v := request_json.get("ponto_referencia"):
                reclamacao.ponto_referencia = v
            if v := request_json.get("bairro"):
                reclamacao.bairro = v
            if v := request_json.get("cidade"):
                reclamacao.cidade = v
            if v := request_json.get("estado"):
                reclamacao.estado = v
            if v := request_json.get("latitude"):
                reclamacao.latitude = v
            if v := request_json.get("longitude"):
                reclamacao.longitude = v
            if request_json.get("longitude") or request_json.get("latitude"):
                reclamacao.geog = func.ST_SetSRID(
                    func.ST_MakePoint(
                        request_json.get("longitude"), request_json.get("latitude")
                    ),
                    4326,
                )
            if v := request_json.get("status"):
                reclamacao.status = v
                reclamacao.atualizacao_status = datetime.now()
            db_session.add(reclamacao)
            db_session.commit()
            return self.reclamacao_json_editar(reclamacao), 200
        except NoResultFound:
            return {"msg": "reclamacao nao encontrada"}, 404
        except:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def delete(self) -> Tuple[Dict[str, str], int]:
        try:
            reclamacao = (
                db_session.query(ReclamacaoEntity)
                .filter(
                    ReclamacaoEntity.id == request.args.get("id"),
                    ReclamacaoEntity.delete == False,
                    ReclamacaoEntity.usuario_id == request.token_id,
                )
                .one()
            )
            reclamacao.delete = True
            reclamacao.modificacao = datetime.now()
            db_session.add(reclamacao)
            db_session.commit()
            return {"msg": "deletado"}, 200
        except NoResultFound:
            return {"msg": "reclamacao nao encontrada"}, 404
        except:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def minhas_reclamacoes(self) -> Tuple[List[Dict[str, str]], int]:
        try:
            LIMIT: int = 10
            page: int = int(request.args.get("page"))
            query = db_session.query(
                ReclamacaoEntity.status,
                ReclamacaoEntity.id,
                ReclamacaoEntity.descricao,
                ReclamacaoEntity.fotos,
                ReclamacaoEntity.endereco,
                ReclamacaoEntity.numero_endereco,
                ReclamacaoEntity.categoria,
                ReclamacaoEntity.qtd_curtidas,
                UsuarioEntity.nome,
                UsuarioEntity.foto,
            ).join(UsuarioEntity, ReclamacaoEntity.usuario_id == UsuarioEntity.id)
            if v := request.args.get("categoria"):
                if v not in [i for i in Categoria.__dict__.keys() if i[:1] != "_"]:
                    return {"msg": "categoria invalida"}, 409
                query = query.filter(
                    ReclamacaoEntity.categoria == v,
                    ReclamacaoEntity.usuario_id == request.token_id,
                    ReclamacaoEntity.delete == False,
                )
            else:
                query = query.filter(
                    ReclamacaoEntity.usuario_id == request.token_id,
                    ReclamacaoEntity.delete == False,
                )
            reclamacoes = (
                query.order_by(
                    ReclamacaoEntity.criacao.desc(),
                )
                .offset(page * LIMIT)
                .limit(LIMIT)
                .all()
            )
            return [
                self.reclamacao_json_feed_pessoal(reclamacao, page)
                for reclamacao in reclamacoes
            ], 200
        except:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def reclamacoes_proximas(self) -> Tuple[List[Dict[str, str]], int]:
        try:
            LIMIT: int = 10
            page: int = int(request.args.get("page"))
            reclamacoes = (
                db_session.query(
                    ReclamacaoEntity.status,
                    ReclamacaoEntity.id,
                    ReclamacaoEntity.descricao,
                    ReclamacaoEntity.fotos,
                    ReclamacaoEntity.endereco,
                    ReclamacaoEntity.numero_endereco,
                    ReclamacaoEntity.categoria,
                    ReclamacaoEntity.qtd_curtidas,
                    UsuarioEntity.nome,
                    UsuarioEntity.foto,
                    CurtidaEntity.delete.label("curtida"),
                )
                .join(UsuarioEntity, ReclamacaoEntity.usuario_id == UsuarioEntity.id)
                .join(
                    CurtidaEntity,
                    and_(
                        CurtidaEntity.usuario_id == request.token_id,
                        CurtidaEntity.reclamacao_id == ReclamacaoEntity.id,
                    ),
                    isouter=True,
                )
                .filter(
                    ReclamacaoEntity.delete == False,
                    ReclamacaoEntity.status == "nao_resolvido",
                    ReclamacaoEntity.categoria == request.args.get("categoria"),
                    func.ST_DWithin(
                        ReclamacaoEntity.geog,
                        func.ST_SetSRID(
                            func.ST_MakePoint(
                                float(request.args.get("longitude")),
                                float(request.args.get("latitude")),
                            ),
                            4326,
                        ),
                        70,
                    ),
                )
                .order_by(
                    func.ST_Distance(
                        ReclamacaoEntity.geog,
                        func.ST_MakePoint(
                            float(request.args.get("longitude")),
                            float(request.args.get("latitude")),
                        ),
                    ),
                    ReclamacaoEntity.qtd_curtidas.desc(),
                    ReclamacaoEntity.criacao.desc(),
                )
                .offset(page * LIMIT)
                .limit(LIMIT)
                .all()
            )
            return [
                self.reclamacao_json_feed(reclamacao, page)
                for reclamacao in reclamacoes
            ], 200
        except:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def reclamacao_json(
        self, reclamacao: ReclamacaoEntity, usuario: UsuarioEntity, curtida: CurtidaEntity
    ) -> Dict[str, str]:
        return {
            "id": reclamacao.id,
            "criacao": reclamacao.criacao,
            "descricao": reclamacao.descricao,
            "categoria": reclamacao.categoria.value,
            "data": reclamacao.data,
            "cep": reclamacao.cep,
            "endereco": reclamacao.endereco,
            "numero_endereco": reclamacao.numero_endereco,
            "ponto_referencia": reclamacao.ponto_referencia,
            "bairro": reclamacao.bairro,
            "cidade": reclamacao.cidade,
            "estado": reclamacao.estado.value,
            "latitude": reclamacao.latitude,
            "longitude": reclamacao.longitude,
            "fotos": reclamacao.fotos.split("|"),
            "qtd_curtidas": reclamacao.qtd_curtidas,
            "status": reclamacao.status.value,
            "nome_usuario": usuario.nome,
            "foto_usuario": usuario.foto,
            "curtido": curtida == False,
        }

    def reclamacao_json_editar(self, reclamacao: ReclamacaoEntity) -> Dict[str, str]:
        return {
            "id": reclamacao.id,
            "criacao": reclamacao.criacao,
            "descricao": reclamacao.descricao,
            "categoria": reclamacao.categoria.value,
            "data": reclamacao.data,
            "cep": reclamacao.cep,
            "endereco": reclamacao.endereco,
            "numero_endereco": reclamacao.numero_endereco,
            "ponto_referencia": reclamacao.ponto_referencia,
            "bairro": reclamacao.bairro,
            "cidade": reclamacao.cidade,
            "estado": reclamacao.estado.value,
            "latitude": reclamacao.latitude,
            "longitude": reclamacao.longitude,
            "fotos": reclamacao.fotos.split("|"),
            "qtd_curtidas": reclamacao.qtd_curtidas,
            "status": reclamacao.status.value,
        }

    def reclamacao_json_feed_pessoal(self, reclamacao, page: int) -> Dict[str, str]:
        return {
            "status": reclamacao.status.value,
            "id": reclamacao.id,
            "descricao": reclamacao.descricao,
            "fotos": reclamacao.fotos.split("|"),
            "endereco": reclamacao.endereco,
            "numero_endereco": reclamacao.numero_endereco,
            "categoria": reclamacao.categoria.value,
            "nome_usuario": reclamacao.nome,
            "foto_usuario": reclamacao.foto,
            "page": page,
            "qtd_curtidas": reclamacao.qtd_curtidas,
        }

    def reclamacao_json_feed(self, reclamacao, page: int) -> Dict[str, str]:
        return {
            "status": reclamacao.status.value,
            "id": reclamacao.id,
            "descricao": reclamacao.descricao,
            "fotos": reclamacao.fotos.split("|"),
            "endereco": reclamacao.endereco,
            "numero_endereco": reclamacao.numero_endereco,
            "categoria": reclamacao.categoria.value,
            "nome_usuario": reclamacao.nome,
            "foto_usuario": reclamacao.foto,
            "page": page,
            "qtd_curtidas": reclamacao.qtd_curtidas,
            "curtido": reclamacao.curtida == False,
        }
