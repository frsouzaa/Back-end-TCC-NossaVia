from flask import Flask
from flask_cors import CORS
from src.view.view_list import View_List
from dotenv import load_dotenv
import os


class App():
    app: Flask = Flask(__name__)

    def __init__(self) -> None:
        CORS(self.app)
        self.cadastrar_rotas()
        self.run_App()

    def cadastrar_rotas(self):
        for view in View_List().list:
            self.app.add_url_rule(view.rota, view_func=view.as_view(view.name))

    def run_App(self) -> None:
        self.app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=False)


if __name__ == "__main__":
    load_dotenv()
    App()
