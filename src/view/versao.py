from flask.views import View as FlaskView
from flask import Response
from typing import List
import json


class Versao(FlaskView):
    rota: str = "/"
    methods: List[str] = ["get"]
    name: str = __name__

    def dispatch_request(self) -> Response:
        with open('image.json', 'r') as file:
            image = json.load(file)
        return f"A aplicação está rodando na versão {image.get("tag")}", 200
