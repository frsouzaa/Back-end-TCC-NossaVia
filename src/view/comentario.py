from flask.views import View as FlaskView
from flask import Response, request
from typing import List, Tuple, Dict
from ..controller.comentario import Comentario as ComentarioController
from ..decorators.validar_token import ValidarToken
from ..decorators.validar_request import ValidarRequest


class Comentario(FlaskView):
    rota: str = "/comentario"
    methods: List[str] = ["post", "get", "delete"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        if request.method == "POST":
            return self.post()
        if request.method == "GET":
            return self.get()
        if request.method == "DELETE":
            return self.delete()

    @ValidarRequest(
        {
            "reclamacao": {"type": "string", "empty": False, "required": True},
            "texto": {"type": "string", "empty": False, "required": True},
        }
    )
    @ValidarToken()
    def post(self) -> Tuple[Dict[str, str], int]:
        return ComentarioController().post()
    
    @ValidarRequest(
        args={
            "reclamacao": {"type": "string", "empty": False, "required": True},
            "page": {"type": "string", "empty": False, "required": True},
        }
    )
    def get(self) -> Tuple[Dict[str, str], int]:
        return ComentarioController().get()

    @ValidarRequest(
        args={
            "id": {"type": "string", "empty": False, "required": True},
        }
    )
    @ValidarToken()
    def delete(self) -> Tuple[Dict[str, str], int]:
        return ComentarioController().delete()
