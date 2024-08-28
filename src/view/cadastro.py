from flask.views import View as FlaskView
from flask import Response
from typing import List, Tuple, Dict
from ..controller.cadastro import Cadastro as CadastroController
from ..db.database import db_session


class Cadastro(FlaskView):
    rota: str = "/cadastro"
    methods: List[str] = ["post"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        return self.post()

    def post(self) -> Tuple[Dict[str, str], int]:
        return CadastroController().post(db_session)
