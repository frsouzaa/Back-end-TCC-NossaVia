from typing import Tuple, Dict
from ..decorators.validar_request import ValidarRequest
from ..db.database import Usuario as UsuarioModel
from flask import request
from psycopg2.errors import UniqueViolation
from ..utils.senha import criptografar
from ..db.database import db_session
from sqlalchemy.orm.exc import NoResultFound


class Usuario:

    def post(self) -> Tuple[str, int]:
        request_json: Dict[str, str] = request.get_json()
        usuario: UsuarioModel = UsuarioModel(
            request_json["nome"],
            request_json["email"],
            criptografar(request_json["senha"]),
            request_json["endereco"],
            request_json["numero_endereco"],
            request_json["complemento_endereco"],
            request_json["cep"],
            request_json["data_nascimento"],
            0,
        )
        try:
            db_session.add(usuario)
            db_session.commit()
            return "criado", 201
        except Exception as e:
            if isinstance(e.orig, UniqueViolation):
                return "email ja cadastrado", 409
            return "ocorreu um erro desconhecido", 520

    def get(self, id):
        if id != request.token_id:
            return "Não autorizado", 401
        try:
            usuario = (
                db_session.query(UsuarioModel)
                .filter(UsuarioModel.id == id, UsuarioModel.delete == False)
                .one()
            )
            return {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "endereco": usuario.endereco,
                "numero_endereco": usuario.numero_endereco,
                "complemento_endereco": usuario.complemento_endereco,
                "cep": usuario.cep,
                "data_nascimento": usuario.data_nascimento,
                "pontucao": usuario.pontucao,
            }, 200
        except NoResultFound:
            return "usuario nao encontrado", 404
        except:
            return "ocorreu um erro desconhecido", 520

    def put(self, id):
        if id != request.token_id:
            return "Não autorizado", 401
        try:
            usuario = (
                db_session.query(UsuarioModel)
                .filter(UsuarioModel.id == id, UsuarioModel.delete == False)
                .one()
            )
            request_json = request.get_json()
            if "nome" in request_json:
                usuario.nome = request_json["nome"]
            if "senha" in request_json:
                usuario.senha = criptografar(request_json["senha"])
            if "endereco" in request_json:
                usuario.endereco = request_json["endereco"]
            if "numero_endereco" in request_json:
                usuario.numero_endereco = request_json["numero_endereco"]
            if "complemento_endereco" in request_json:
                usuario.complemento_endereco = request_json["complemento_endereco"]
            if "cep" in request_json:
                usuario.cep = request_json["cep"]
            if "data_nascimento" in request_json:
                usuario.data_nascimento = request_json["data_nascimento"]
            db_session.add(usuario)
            db_session.commit()
            return "atualizado", 200
        except NoResultFound:
            return "usuario nao encontrado", 404
        except:
            return "ocorreu um erro desconhecido", 520

    def delete(self, id):
        if id != request.token_id:
            return "Não autorizado", 401
        try:
            usuario = (
                db_session.query(UsuarioModel)
                .filter(UsuarioModel.id == id, UsuarioModel.delete == False)
                .one()
            )
            usuario.delete = True
            db_session.add(usuario)
            db_session.commit()
            return "deletado", 200
        except NoResultFound:
            return "usuario nao encontrado", 404
        except:
            return "ocorreu um erro desconhecido", 520
