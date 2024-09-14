from typing import List
from .login import Login
from .usuario import Usuario
from .denuncia import Denuncia
from .versao import Versao
from .alterar_senha import AlterarSenha


class View_List():
    list: List

    def __init__(self) -> None:
        self.list = [
            Login(),
            Usuario(),
            Denuncia(),
            Versao(),
            AlterarSenha()
        ]
