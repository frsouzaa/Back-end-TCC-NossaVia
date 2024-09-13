from flask.views import View as FlaskView
from flask import Response
from typing import List, Tuple, Dict
from ..controller.denuncia import Denuncia as DenunciaController
from ..decorators.validar_token import ValidarToken
from ..decorators.validar_request import ValidarRequest


class Denuncia(FlaskView):
    rota: str = "/denuncia"
    methods: List[str] = ["post"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        return self.post()

    @ValidarRequest(
        {
            "titulo": {"type": "string", "empty": False, "required": True},
            "descricao": {"type": "string", "empty": False, "required": True},
            "categoria": {"type": "string", "empty": False, "required": True},
            "data": {"type": "string", "empty": False, "required": True},
            "endereco": {"type": "string", "empty": False, "required": False},
            "numero_endereco": {"type": "string", "empty": False, "required": False},
            "ponto_referencia": {"type": "string", "empty": False, "required": False},
            "cep": {"type": "string", "empty": False, "required": False},
            "latitude": {"type": "string", "empty": False, "required": True},
            "longitude": {"type": "string", "empty": False, "required": True},
            "fotos": {
                "type": "list",
                "schema": {"type": "string"},
                "empty": False,
                "required": True,
            },
        }
    )
    @ValidarToken()
    def post(self) -> Tuple[Dict[str, str], int]:
        return DenunciaController().post()
