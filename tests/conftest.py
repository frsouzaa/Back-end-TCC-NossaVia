import pytest
from app import App
from datetime import datetime
from src.utils.senha import criptografar
from src.db.database import db_session, Usuario, Base, engine, Reclamacao, Comentario
from unittest import mock
import os
from src.utils.jwt import gerar as gerar_token
from sqlalchemy import func


def pytest_sessionstart(session):
    Base.metadata.create_all(engine)
    for i in range(11):
        usuario: Usuario = Usuario(
            f"usuario teste {i}",
            f"{i}2{i}.4{i}6.{i}8{i}-10",
            f"email_{i}@teste.com",
            criptografar(f"senha_{i}"),
            "12345-678",
            "rua teste",
            "123",
            "complemento teste",
            "bairro teste",
            "cidade teste",
            "MG",
            datetime.now(),
            "n",
            "11 11111-1111",
            0,
        )
        db_session.add(usuario)
    db_session.flush()
    for i in range(11):
        latitude = i
        longitude = i
        reclamacao: Reclamacao = Reclamacao(
            f"descricao_{i}",
            "via",
            "2024-10-03 19:47:00.000000",
            "12345-123",
            "rua teste",
            "123",
            "perto do teste",
            "bairro teste",
            "cidade teste",
            "PI",
            latitude,
            longitude,
            "",
            0,
            i + 1,
            "nao_resolvido",
            None,
            func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),
        )
        db_session.add(reclamacao)
    db_session.flush()
    for i in range(11):
        comentario: Comentario = Comentario(
            f"comentario teste {i}",
            i + 1,
            i + 1,
        )
        db_session.add(comentario)
    db_session.commit()


@pytest.fixture(scope="session")
def app():
    app = App()
    app.cadastrar_rotas()
    app.app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture(scope="session")
def client(app):
    return app.app.test_client()


@pytest.fixture(scope="session")
def database_session():
    return db_session


@pytest.fixture(scope="function")
def login(client):
    def logar(email: str, senha: str):
        response = client.post("/login", json={"email": email, "senha": senha})
        return response.json.get("token")

    return logar


@pytest.fixture(scope="function")
def token_falso():
    def gerar_token_falso(id):
        with mock.patch.dict(os.environ, {"JWT_KEY": "CHAVE_TESTE"}):
            return gerar_token({"id": str(id)})

    return gerar_token_falso
