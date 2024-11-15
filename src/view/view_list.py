from typing import List
from .login import Login
from .usuario import Usuario
from .reclamacao import Reclamacao
from .versao import Versao
from .alterar_senha import AlterarSenha
from .minhas_reclamacoes import MinhasReclamacaos
from .recuperar_senha import RecuperarSenha
from .reclamacoes_proximas import ReclamacoesProximas
from .curtida import Curtida
from .comentario import Comentario
from .localizacao import Localizacao


class View_List:
    list: List

    def __init__(self) -> None:
        self.list = [
            Login(),
            Usuario(),
            Reclamacao(),
            Versao(),
            AlterarSenha(),
            MinhasReclamacaos(),
            RecuperarSenha(),
            ReclamacoesProximas(),
            Curtida(),
            Comentario(),
            Localizacao()
        ]
