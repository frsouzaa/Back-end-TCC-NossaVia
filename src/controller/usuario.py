from typing import Tuple, Dict
from ..db.database import Usuario as UsuarioModel
from flask import request
from psycopg2.errors import UniqueViolation
from psycopg2.errors import InvalidTextRepresentation
from ..utils.senha import criptografar
from ..db.database import db_session
from sqlalchemy.orm.exc import NoResultFound
from ..utils.azure import upload_blob
from uuid import uuid4
from os import getenv
import time


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
            request_json["sexo"],
            request_json["telefone"],
            0,
        )
        try:
            db_session.add(usuario)
            db_session.commit()
            return {"msg": "criado"}, 201
        except Exception as e:
            if isinstance(e.orig, UniqueViolation):
                return {"msg": "email ja cadastrado"}, 409
            if isinstance(e.orig, InvalidTextRepresentation):
                return {"msg": "categoria invalida"}, 409
            return {"msg": "ocorreu um erro desconhecido"}, 520

    def get(self):
        try:
            usuario = (
                db_session.query(UsuarioModel)
                .filter(
                    UsuarioModel.id == request.token_id, UsuarioModel.delete == False
                )
                .one()
            )
            return self.usuario_json(usuario), 200
        except NoResultFound:
            return {"msg": "usuario nao encontrado"}, 404
        except:
            return {"msg": "ocorreu um erro desconhecido"}, 520

    def put(self):
        try:
            usuario = (
                db_session.query(UsuarioModel)
                .filter(
                    UsuarioModel.id == request.token_id, UsuarioModel.delete == False
                )
                .one()
            )
            request_json = request.get_json()
            if not request_json:
                return {"msg": "nada foi alterado"}, 200
            if "nome" in request_json:
                usuario.nome = request_json["nome"]
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
            if "sexo" in request_json:
                usuario.sexo = request_json["sexo"]
            if "telefone" in request_json:
                usuario.telefone = request_json["telefone"]
            if "foto" in request_json:
                if not request_json["foto"]:
                    usuario.foto = None
                else:
                    foto_base64: str = request_json["foto"]
                    nome: str = f"imagem_{uuid4()}.jpg"
                    upload_blob(foto_base64, nome)
                    usuario.foto = f"{getenv('AZURE_BLOB_URL')}/{nome}"
            db_session.add(usuario)
            db_session.commit()
            return self.usuario_json(usuario), 200
        except NoResultFound:
            return {"msg": "usuario nao encontrado"}, 404
        except:
            return {"msg": "ocorreu um erro desconhecido"}, 520

    def delete(self):
        try:
            usuario = (
                db_session.query(UsuarioModel)
                .filter(
                    UsuarioModel.id == request.token_id, UsuarioModel.delete == False
                )
                .one()
            )
            usuario.delete = True
            usuario.email = f"{usuario.email}_deletado_{int(time.time())}"
            db_session.add(usuario)
            db_session.commit()
            return {"msg": "deletado"}, 200
        except NoResultFound:
            return {"msg": "usuario nao encontrado"}, 404
        except:
            return {"msg": "ocorreu um erro desconhecido"}, 520

    def usuario_json(self, usuario: UsuarioModel) -> Dict[str, str]:
        return {
            "nome": usuario.nome,
            "email": usuario.email,
            "endereco": usuario.endereco,
            "numero_endereco": usuario.numero_endereco,
            "complemento_endereco": usuario.complemento_endereco,
            "cep": usuario.cep,
            "data_nascimento": usuario.data_nascimento.strftime("%Y-%m-%d %H:%M:%S:%f"),
            "sexo": usuario.sexo.value,
            "telefone": usuario.telefone,
            "pontucao": usuario.pontucao,
            "foto": usuario.foto,
        }
