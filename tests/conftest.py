import docker
from time import sleep

print("Iniciando container do PostgreSQL para realização dos testes")

docker_client = docker.DockerClient()
container = docker_client.containers.run(
    "postgres:16",
    environment={
        "POSTGRES_DB": "test_db",
        "POSTGRES_USER": "test_user",
        "POSTGRES_PASSWORD": "test_pass",
    },
    ports={"5432/tcp": "12345"},
    detach=True,
    auto_remove=True,
    remove=True,
)

while container.exec_run("pg_isready").exit_code != 0:
    sleep(0.5)

import pytest
from app import App
from datetime import datetime
from src.utils.senha import criptografar
from src.db.database import db_session, Usuario, Base, engine, Denuncia
from unittest import mock
import os
from src.utils.jwt import gerar as gerar_token

Base.metadata.create_all(engine)

print("Container de testes inicializado e configurado com sucesso")


def pytest_sessionstart(session):
    for i in range(11):
        usuario: Usuario = Usuario(
            f"usuario teste {i}",
            f"email_{i}@teste.com",
            criptografar(f"senha_{i}"),
            "rua teste",
            "123",
            "complemento teste",
            "12345-678",
            datetime.now(),
            "n",
            "11 11111-1111",
            0,
        )
        db_session.add(usuario)
    db_session.flush()
    for i in range(11):
        denuncia: Denuncia = Denuncia(
            f"descricao_{i}",
            "via",
            "2024-10-03 19:47:00.000000",
            "rua teste",
            "123",
            "perto do teste",
            "12345-123",
            "-1234567890",
            "-1234567890",
            "",
            0,
            i+1,
            "nao_resolvido",
            None,
        )
        db_session.add(denuncia)
    db_session.commit()


def pytest_sessionfinish(session, exitstatus):
    container.kill()
    container.wait(condition="removed")


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
