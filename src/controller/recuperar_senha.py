from typing import Tuple, Dict
from ..db.database import RecuperarSenha as RecuperarSenhaEntity
from ..db.database import Usuario as UsuarioEntity
from flask import request
from ..db.database import db_session
import traceback
from random import randint
from ..utils.email import enviar
from datetime import datetime, timedelta
from ..utils.senha import criptografar
from sqlalchemy.sql import exists

class RecuperarSenha:
    
    TEMPO_TOKEN = 15

    def post(self) -> Tuple[Dict[str, str] | str, int]:
        try:
            request_json: Dict[str, str] = request.get_json()
            usuario = (
                db_session.query(UsuarioEntity)
                .filter(
                    UsuarioEntity.email == request_json["email"],
                )
                .all()
            )

            if not usuario:
                return {"msg": "email nao encontrado"}, 409

            tokens = (
                db_session.query(RecuperarSenhaEntity)
                .join(
                    UsuarioEntity, UsuarioEntity.id == RecuperarSenhaEntity.usuario_id
                )
                .filter(
                    RecuperarSenhaEntity.usuario_id == usuario[0].id,
                    RecuperarSenhaEntity.delete == False,
                )
                .all()
            )
            for token in tokens:
                token.delete = True
                token.modificacao = datetime.now()
                db_session.add(token)
            new_token = RecuperarSenhaEntity(
                str(randint(100000, 999999)), usuario[0].id
            )
            db_session.add(new_token)
            db_session.flush()
            res = enviar(
                request_json["email"],
                "Recuperação de senha",
                f"Seu token para recuperação de senha é: {new_token.token}",
            )
            if not res:
                db_session.rollback()
                return {"msg": "nao foi possivel enviar o email nesse momento"}, 520
            db_session.commit()
            return {"msg": "token gerado"}, 200
        except Exception as e:
            db_session.rollback()
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()
            
    def get(self) -> Tuple[Dict[str, str] | str, int]:
        try:
            dados = (
                db_session.query(RecuperarSenhaEntity.token)
                .join(
                    UsuarioEntity,
                    UsuarioEntity.id == RecuperarSenhaEntity.usuario_id,
                )
                .filter(
                    RecuperarSenhaEntity.token == request.args.get("token"),
                    RecuperarSenhaEntity.criacao
                    > (datetime.now() - timedelta(minutes=self.TEMPO_TOKEN)).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    RecuperarSenhaEntity.delete == False,
                    UsuarioEntity.email == request.args.get("email"),
                    UsuarioEntity.delete == False,
                )
                .scalar()
            )
            if not dados:
                return {"msg": "token ou email incorreto"}, 409
            return {"msg": "token valido"}, 200
        except Exception as e:
            db_session.rollback()
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def put(self) -> Tuple[Dict[str, str] | str, int]:
        request_json: Dict[str, str] = request.get_json()
        try:
            dados = (
                db_session.query(UsuarioEntity, RecuperarSenhaEntity)
                .join(
                    RecuperarSenhaEntity,
                    RecuperarSenhaEntity.usuario_id == UsuarioEntity.id,
                )
                .filter(
                    RecuperarSenhaEntity.token == request_json["token"],
                    RecuperarSenhaEntity.criacao
                    > (datetime.now() - timedelta(minutes=self.TEMPO_TOKEN)).strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    RecuperarSenhaEntity.delete == False,
                    UsuarioEntity.email == request_json["email"],
                    UsuarioEntity.delete == False,
                )
                .all()
            )
            if not dados:
                return {"msg": "token ou email incorreto"}, 400
            dados[0][0].senha = criptografar(request_json["senhaNova"])
            dados[0][0].modificacao = datetime.now()
            dados[0][1].delete = True
            dados[0][1].modificacao = datetime.now()
            db_session.add(dados[0][1])
            db_session.commit()
            return {"msg": "senha alterada"}, 200
        except Exception as e:
            db_session.rollback()
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()
