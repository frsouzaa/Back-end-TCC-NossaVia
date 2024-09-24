import pytest
from src.db.database import Usuario, engine, Base, db_session
from app import App
from datetime import datetime
from src.utils.senha import criptografar


@pytest.fixture(scope="session")
def session():
    if not engine.url.get_backend_name() == "sqlite":
        raise RuntimeError(
            "Altere o valor da variável de ambiente DB_URI no arquivo pytest.ini para um banco de dados sqlite"
        )

    Base.metadata.create_all(engine)
    try:
        yield db_session
    finally:
        Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def seed(session):
    for i in range(1):
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
        usuario.id = i
        session.add(usuario)
    session.commit()


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
def runner(app):
    return app.app.test_cli_runner()
