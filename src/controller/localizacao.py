from typing import Tuple, Dict
from flask import request
import traceback
import requests
import os


class Localizacao:

    def get_viacep(self) -> Tuple[Dict[str, str] | str, int]:
        try:
            response = requests.get(f"https://viacep.com.br/ws/{request.args['cep']}/json/")
            return response.json(), response.status_code
        except Exception as e:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520

    def get_geocode(self) -> Tuple[Dict[str, str] | str, int]:
        try:
            response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={request.args['endereco']}&key={os.getenv('GOOGLE_API_KEY')}")
            return {
                "latitude": response.json().get("results", [{}])[0].get("geometry", {}).get("location", {}).get("lat", None),
                "longitude": response.json().get("results", [{}])[0].get("geometry", {}).get("location", {}).get("lng", None)
            }, response.status_code
        except Exception as e:
            print(traceback.format_exc())
            return {"msg": "ocorreu um erro desconhecido"}, 520
