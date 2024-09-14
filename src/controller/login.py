from typing import Tuple, Dict
from ..decorators.validar_request import ValidarRequest
from ..db.database import Usuario as UsuarioModel
from flask import jsonify, request
from ..utils.senha import descriptografar
from ..utils.jwt import gerar as gerar_jwt


class Login:

    @ValidarRequest(
        {
            "email": {"type": "string", "empty": False, "required": True},
            "senha": {"type": "string", "empty": False, "required": True},
        }
    )
    def post(self) -> Tuple[Dict[str, str] | str, int]:
        request_json: Dict[str, str] = request.get_json()
        usuario = UsuarioModel.query.filter(
            UsuarioModel.email == request_json["email"], UsuarioModel.delete == False
        ).first()
        if not usuario or not descriptografar(request_json["senha"], usuario.senha):
            return {"msg": "usuário ou senha incorretos"}, 401
        return jsonify(self.usuario_json(usuario)), 200

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
            "token": gerar_jwt({"id": str(usuario.id)}),
        }
