from flask.views import View as FlaskView
from flask import Response, request
from typing import List, Tuple, Dict
from ..controller.curtida import Curtida as CurtidaController
from ..decorators.validar_token import ValidarToken
from ..decorators.validar_request import ValidarRequest


class Curtida(FlaskView):
    rota: str = "/curtida"
    methods: List[str] = ["post", "delete"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        if request.method == "POST":
            return self.post()
        if request.method == "DELETE":
            return self.delete()

    @ValidarRequest(
        {
            "reclamacao": {"type": "string", "empty": False, "required": True},
        }
    )
    @ValidarToken()
    def post(self) -> Tuple[Dict[str, str], int]:
        return CurtidaController().post()

    @ValidarRequest(
        args={
            "reclamacao": {"type": "string", "empty": False, "required": True},
        }
    )
    @ValidarToken()
    def delete(self) -> Tuple[Dict[str, str], int]:
        return CurtidaController().delete()
