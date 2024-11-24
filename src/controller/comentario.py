from typing import Dict, Tuple
from ..db.database import db_session
from ..db.database import Comentario as ComentarioModel
from ..db.database import Usuario as UsuarioModel
from ..db.database import Reclamacao as ReclamacaoModel
import traceback
from flask import request
from datetime import datetime
from ..utils.pontuacao import atualizar as atualizar_pontuacao
from os import getenv


class Comentario:
    QTD_PONTOS: int = int(getenv("PONTOS_COMENTARIO"))

    def post(self) -> Tuple[Dict[str, str], int]:
        try:
            request_json: Dict[str, str] = request.get_json()
            comentario = ComentarioModel(
                request_json["texto"], request_json["reclamacao"], request.token_id
            )
            db_session.add(comentario)
            db_session.flush()
            db_session.refresh(comentario)
            reclamacao = (
                db_session.query(ReclamacaoModel.usuario_id)
                .filter(ReclamacaoModel.id == request_json["reclamacao"])
                .one()
            )
            if reclamacao.usuario_id != request.token_id:
                atualizar_pontuacao(request.token_id, self.QTD_PONTOS, db_session)
                atualizar_pontuacao(reclamacao.usuario_id, self.QTD_PONTOS, db_session)
            db_session.commit()
            comentario = (
                db_session.query(
                    ComentarioModel.texto,
                    ComentarioModel.criacao,
                    ComentarioModel.id.label("id_comentario"),
                    UsuarioModel.nome,
                    UsuarioModel.foto,
                    UsuarioModel.id.label("id_usuario"),
                )
                .join(UsuarioModel, UsuarioModel.id == ComentarioModel.usuario_id)
                .filter(
                    ComentarioModel.id == comentario.id,
                )
                .one()
            )
            return self.comentario_json(comentario), 201
        except Exception as e:
            if "comentario_reclamacao_id_fkey" in e.orig.pgerror:
                return {"msg": "reclamacao nao encontrada"}, 404
            if "comentario_usuario_id_fkey" in e.orig.pgerror:
                return {"msg": "usuario nao encontrado"}, 404
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.close()

    def get(self) -> Tuple[Dict[str, str], int]:
        LIMIT: int = 10
        try:
            comentarios = (
                db_session.query(
                    ComentarioModel.texto,
                    ComentarioModel.criacao,
                    ComentarioModel.id.label("id_comentario"),
                    UsuarioModel.nome,
                    UsuarioModel.foto,
                    UsuarioModel.id.label("id_usuario"),
                )
                .join(UsuarioModel, UsuarioModel.id == ComentarioModel.usuario_id)
                .filter(
                    ComentarioModel.reclamacao_id == request.args["reclamacao"],
                    ComentarioModel.delete == False,
                    UsuarioModel.delete == False,
                )
                .limit(LIMIT)
                .offset(int(request.args["page"]) * LIMIT)
                .all()
            )
            return [self.comentario_json(comentario) for comentario in comentarios], 200
        except Exception as e:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.close()

    def delete(self) -> Tuple[Dict[str, str], int]:
        try:
            comentario = (
                db_session.query(ComentarioModel)
                .filter(
                    ComentarioModel.id == request.args["id"],
                    ComentarioModel.usuario_id == request.token_id,
                    ComentarioModel.delete == False,
                )
                .one_or_none()
            )
            if not comentario:
                return {"msg": "comentario nao encontrado"}, 404
            comentario.delete = True
            comentario.modificacao = datetime.now()
            db_session.add(comentario)
            db_session.flush()
            reclamacao = (
                db_session.query(ReclamacaoModel.usuario_id)
                .filter(ReclamacaoModel.id == comentario.reclamacao_id)
                .one()
            )
            if reclamacao.usuario_id != request.token_id:
                atualizar_pontuacao(request.token_id, -self.QTD_PONTOS, db_session)
                atualizar_pontuacao(reclamacao.usuario_id, -self.QTD_PONTOS, db_session)
            db_session.commit()
            return {"msg": "comentario deletado com sucesso"}, 200
        except Exception as e:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.close()

    def comentario_json(self, comentario) -> Dict[str, str]:
        return {
            "texto": comentario.texto,
            "criacao": comentario.criacao.strftime("%Y-%m-%d %H:%M:%S:%f"),
            "nome": comentario.nome,
            "foto": comentario.foto,
            "id_usuario": comentario.id_usuario,
            "id_comenatario": comentario.id_comentario,
        }
