from typing import Tuple, Dict
from flask import request
from ..db.database import Curtida as CurtidaModel
from ..db.database import Reclamacao as ReclamacaoModel
from ..db.database import db_session
from datetime import datetime
import traceback
from ..utils.pontuacao import atualizar as atualizar_pontuacao
from os import getenv


class Curtida:
    QTD_PONTOS: int = int(getenv("PONTOS_CURTIDA"))

    def post(self) -> Tuple[Dict[str, str], int]:
        try:
            request_json = request.get_json()
            existente = (
                db_session.query(ReclamacaoModel, CurtidaModel)
                .join(CurtidaModel, ReclamacaoModel.id == CurtidaModel.reclamacao_id)
                .filter(
                    CurtidaModel.usuario_id == request.token_id,
                    CurtidaModel.reclamacao_id == request_json["reclamacao"],
                )
                .one_or_none()
            )
            if existente:
                if not existente[1].delete:
                    return {"mensagem": "reclamacao ja curtida pelo usuario"}, 409
                existente[1].delete = False
                existente[1].modificacao = datetime.now()
                existente[0].qtd_curtidas += 1
                existente[0].modificacao = datetime.now()
                db_session.add(existente[0])
                db_session.add(existente[1])
                db_session.flush()
                if existente[0].usuario_id != request.token_id:
                    atualizar_pontuacao(request.token_id, self.QTD_PONTOS, db_session)
                    atualizar_pontuacao(existente[0].usuario_id, self.QTD_PONTOS, db_session)
                db_session.commit()
                return {"mensagem": "curtida realizada com sucesso"}, 200
            reclamacao = (
                db_session.query(ReclamacaoModel)
                .filter(
                    ReclamacaoModel.id == request_json["reclamacao"],
                )
                .one_or_none()
            )
            if not reclamacao:
                return {"mensagem": "reclamacao nao encontrada"}, 404
            curtida = CurtidaModel(request.token_id, request_json["reclamacao"])
            reclamacao.qtd_curtidas += 1
            reclamacao.modificacao = datetime.now()
            db_session.add(reclamacao)
            db_session.add(curtida)
            db_session.flush()
            if reclamacao.usuario_id != request.token_id:
                atualizar_pontuacao(request.token_id, self.QTD_PONTOS, db_session)
                atualizar_pontuacao(reclamacao.usuario_id, self.QTD_PONTOS, db_session)
            db_session.commit()
            return {"mensagem": "curtida realizada com sucesso"}, 201
        except Exception as e:
            print(traceback.format_exc())
            return {"mensagem": "erro desconhecido"}, 520
        finally:
            db_session.remove()

    def delete(self) -> Tuple[Dict[str, str], int]:
        try:
            existente = (
                db_session.query(ReclamacaoModel, CurtidaModel)
                .join(CurtidaModel, ReclamacaoModel.id == CurtidaModel.reclamacao_id)
                .filter(
                    CurtidaModel.usuario_id == request.token_id,
                    CurtidaModel.reclamacao_id == request.args.get("reclamacao"),
                )
                .one_or_none()
            )
            if not existente or existente[1].delete:
                return {"mensagem": "reclamacao nao estava curtida pelo usuario"}, 409
            existente[1].delete = True
            existente[1].modificacao = datetime.now()
            existente[0].qtd_curtidas -= 1
            existente[0].modificacao = datetime.now()
            db_session.add(existente[0])
            db_session.add(existente[1])
            db_session.flush()
            if existente[0].usuario_id != request.token_id:
                atualizar_pontuacao(request.token_id, -self.QTD_PONTOS, db_session)
                atualizar_pontuacao(existente[0].usuario_id, -self.QTD_PONTOS, db_session)
            db_session.commit()
            return {"mensagem": "curtida removida com sucesso"}, 200
        except Exception as e:
            print(traceback.format_exc())
            return {"mensagem": "erro desconhecido"}, 520
        finally:
            db_session.remove()
