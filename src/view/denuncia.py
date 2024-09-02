from flask.views import View as FlaskView
from flask import Response
from typing import List, Tuple, Dict
from ..controller.denuncia import Denuncia as DenunciaController


class Denuncia(FlaskView):
    rota: str = "/denuncia"
    methods: List[str] = ["post"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        return self.post()

    def post(self) -> Tuple[Dict[str, str], int]:
        return DenunciaController().post()
