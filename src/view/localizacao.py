from flask.views import View as FlaskView
from flask import Response
from typing import List, Tuple, Dict
from ..controller.localizacao import Localizacao as LocalizacaoControler
from ..decorators.validar_request import ValidarRequest


class Localizacao(FlaskView):
    rota: str = "/localizacao/<modo>"
    methods: List[str] = ["get"]
    name: str = __name__

    def dispatch_request(self, modo: str) -> Response:
        if modo == "viacep":
            return self.get_viacep()
        if modo == "geocode":
            return self.get_geocode()

    @ValidarRequest(
        args={
            "cep": {"type": "string", "empty": False, "required": True},
        }
    )
    def get_viacep(self) -> Tuple[Dict[str, str], int]:
        return LocalizacaoControler().get_viacep()

    @ValidarRequest(
        args={
            "endereco": {"type": "string", "empty": False, "required": True},
        }
    )
    def get_geocode(self) -> Tuple[Dict[str, str], int]:
        return LocalizacaoControler().get_geocode()
