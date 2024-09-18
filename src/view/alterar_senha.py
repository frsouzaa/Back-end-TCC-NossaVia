from flask.views import View as FlaskView
from flask import Response
from typing import List, Tuple, Dict
from ..controller.alterar_senha import AlterarSenha as AlterarSenhaController
from ..decorators.validar_request import ValidarRequest
from ..decorators.validar_token import ValidarToken


class AlterarSenha(FlaskView):
    rota: str = "/alterar-senha"
    methods: List[str] = ["post"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        return self.post()

    @ValidarRequest(
        {
            "senhaAtual": {"type": "string", "empty": False, "required": True},
            "senhaNova": {"type": "string", "empty": False, "required": True},
        }
    )
    @ValidarToken()
    def post(self) -> Tuple[Dict[str, str], int]:
        return AlterarSenhaController().post()