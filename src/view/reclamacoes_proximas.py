from flask.views import View as FlaskView
from flask import Response
from typing import List, Tuple, Dict
from ..controller.reclamacao import Reclamacao as ReclamacaoController
from ..decorators.validar_token import ValidarToken
from ..decorators.validar_request import ValidarRequest


class ReclamacoesProximas(FlaskView):
    rota: str = "/reclamacoes-proximas"
    methods: List[str] = ["get"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        return self.get()

    @ValidarRequest(
        args={
            "latitude": {"type": "string", "empty": False, "required": True},
            "longitude": {"type": "string", "empty": False, "required": True},
            "page": {"type": "string", "empty": False, "required": True},
            "categoria": {"type": "string", "empty": False, "required": True},
        }
    )
    @ValidarToken()
    def get(self) -> Tuple[Dict[str, str], int]:
        return ReclamacaoController().reclamacoes_proximas()
