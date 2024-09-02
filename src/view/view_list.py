from typing import List
from .login import Login
from .cadastro import Cadastro
from .denuncia import Denuncia
from .versao import Versao


class View_List():
    list: List

    def __init__(self) -> None:
        self.list = [
            Login(),
            Cadastro(),
            Denuncia(),
            Versao()
        ]
