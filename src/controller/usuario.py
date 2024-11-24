from typing import Tuple, Dict
from ..db.database import Usuario as UsuarioModel
from flask import request
from psycopg2.errorcodes import INVALID_TEXT_REPRESENTATION
from ..utils.senha import criptografar
from ..db.database import db_session
from sqlalchemy.orm.exc import NoResultFound
from ..utils.azure import upload_blob
from uuid import uuid4
from os import getenv
import time
from datetime import datetime
import traceback


class Usuario:

    def post(self) -> Tuple[str, int]:
        try:
            request_json: Dict[str, str] = request.get_json()
            usuario: UsuarioModel = UsuarioModel(
                request_json["nome"],
                request_json["cpf"],
                request_json["email"],
                criptografar(request_json["senha"]),
                request_json["cep"],
                request_json["endereco"],
                request_json["numero_endereco"],
                request_json["complemento_endereco"],
                request_json["bairro"],
                request_json["cidade"],
                request_json["estado"],
                datetime.strptime(request_json["data_nascimento"], "%Y-%m-%d %H:%M:%S.%f"),
                request_json["sexo"],
                request_json["telefone"],
                0,
            )
            db_session.add(usuario)
            db_session.commit()
            return {"msg": "criado"}, 201
        except Exception as e:
            db_session.rollback()
            if "usuario_cpf_key" in e.orig.pgerror:
                return {"msg": "cpf ja cadastrado"}, 409
            if "usuario_email_key" in e.orig.pgerror:
                return {"msg": "email ja cadastrado"}, 409
            if e.orig.pgcode == INVALID_TEXT_REPRESENTATION:
                return {"msg": "sexo invalido"}, 409
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

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
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def put(self):
        try:
            request_json = request.get_json()
            usuario = (
                db_session.query(UsuarioModel)
                .filter(
                    UsuarioModel.id == request.token_id, UsuarioModel.delete == False
                )
                .one()
            )
            if not request_json:
                return {"msg": "nada foi alterado"}, 200
            if v := request_json.get("nome"):
                usuario.nome = v
            if v := request_json.get("cep"):
                usuario.cep = v
            if v := request_json.get("endereco"):
                usuario.endereco = v
            if v := request_json.get("numero_endereco"):
                usuario.numero_endereco = v
            if v := request_json.get("complemento_endereco"):
                usuario.complemento_endereco = v
            if v := request_json.get("bairro"):
                usuario.bairro = v
            if v := request_json.get("cidade"):
                usuario.cidade = v
            if v := request_json.get("estado"):
                usuario.estado = v
            if v := request_json.get("data_nascimento"):
                usuario.data_nascimento = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
            if v := request_json.get("sexo"):
                usuario.sexo = v
            if v := request_json.get("telefone"):
                usuario.telefone = v
            if "foto" in request_json:
                if not request_json["foto"]:
                    usuario.foto = None
                else:
                    foto_base64: str = request_json["foto"]
                    nome: str = f"imagem_{uuid4()}.jpg"
                    usuario.foto = f"{getenv('AZURE_BLOB_URL')}/{getenv('AZURE_BLOB_CONTAINER_USUARIOS')}/{nome}"
            db_session.add(usuario)
            db_session.flush()
            if request_json.get("foto"):
                upload_blob(foto_base64, nome, getenv("AZURE_BLOB_CONTAINER_USUARIOS"))
            db_session.commit()
            return self.usuario_json(usuario), 200
        except NoResultFound:
            return {"msg": "usuario nao encontrado"}, 404
        except:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

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
            usuario.cpf = f"{usuario.cpf}_deletado_{int(time.time())}"
            usuario.modificacao = datetime.now()
            db_session.add(usuario)
            db_session.commit()
            return {"msg": "deletado"}, 200
        except NoResultFound:
            return {"msg": "usuario nao encontrado"}, 404
        except:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
        finally:
            db_session.remove()

    def usuario_json(self, usuario: UsuarioModel) -> Dict[str, str]:
        return {
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "email": usuario.email,
            "cep": usuario.cep,
            "endereco": usuario.endereco,
            "numero_endereco": usuario.numero_endereco,
            "complemento_endereco": usuario.complemento_endereco,
            "bairro": usuario.bairro,
            "cidade": usuario.cidade,
            "estado": usuario.estado.value,
            "data_nascimento": usuario.data_nascimento.strftime("%Y-%m-%d %H:%M:%S:%f"),
            "sexo": usuario.sexo.value,
            "telefone": usuario.telefone,
            "pontuacao": usuario.pontuacao,
            "foto": usuario.foto,
            "id": usuario.id,
        }
