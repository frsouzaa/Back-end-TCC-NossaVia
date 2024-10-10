from flask.views import View as FlaskView
from flask import Response
from typing import List, Tuple, Dict
from ..controller.denuncia import Denuncia as DenunciaController
from ..decorators.validar_token import ValidarToken
from ..decorators.validar_request import ValidarRequest


class MinhasDenuncias(FlaskView):
    rota: str = "/minhas-denuncias"
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
        return DenunciaController().minhas_denuncias()