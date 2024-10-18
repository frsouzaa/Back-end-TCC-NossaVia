from flask.views import View as FlaskView
from flask import Response
from typing import List, Tuple, Dict
from ..controller.reclamacao import Reclamacao as ReclamacaoController
from ..decorators.validar_token import ValidarToken
from ..decorators.validar_request import ValidarRequest


class MinhasReclamacaos(FlaskView):
    rota: str = "/minhas-reclamacoes"
    methods: List[str] = ["get"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        return self.get()

    @ValidarRequest(
        args={
            "categoria": {"type": "string", "empty": False, "required": False},
            "page": {"type": "string", "empty": False, "required": False},
        }
    )
    @ValidarToken()
    def get(self) -> Tuple[Dict[str, str], int]:
        return ReclamacaoController().minhas_reclamacoes()
