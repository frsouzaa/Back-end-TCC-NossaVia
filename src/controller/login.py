from typing import Tuple, Dict
from ..decorators.validar_request import ValidarRequest
from ..db.database import Usuario as UsuarioModel
from flask import jsonify, request
from ..utils.senha import descriptografar
from ..utils.jwt import gerar as gerar_jwt
import traceback


class Login:

    @ValidarRequest(
        {
            "email": {"type": "string", "empty": False, "required": True},
            "senha": {"type": "string", "empty": False, "required": True},
        }
    )
    def post(self) -> Tuple[Dict[str, str] | str, int]:
        try:
            request_json: Dict[str, str] = request.get_json()
            usuario = UsuarioModel.query.filter(
                UsuarioModel.email == request_json["email"],
                UsuarioModel.delete == False,
            ).first()
            if not usuario or not descriptografar(request_json["senha"], usuario.senha):
                return {"msg": "usuário ou senha incorretos"}, 401
            return jsonify(self.usuario_json(usuario)), 200
        except Exception as e:
            print(traceback.format_exc())
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
            "pontuacao": usuario.pontuacao,
            "foto": usuario.foto,
            "token": gerar_jwt({"id": usuario.id}),
            "bairro": usuario.bairro,
            "cidade": usuario.cidade,
            "estado": usuario.estado.value,
            "id": usuario.id,
        }
