from src.db.database import RecuperarSenha
from src.utils.senha import criptografar


def test_put_recuperar_senha(client, database_session):
    database_session.add(RecuperarSenha(criptografar("123456"), 10))
    response = client.put(
        "/recuperar-senha",
        json={
            "email": "email_9@teste.com",
            "token": "123456",
            "senhaNova": "senha_999",
        },
    )
    assert response.status_code == 200
    assert response.json == {"msg": "senha alterada"}


def test_put_recuperar_senha_email_errado(client, database_session):
    database_session.add(RecuperarSenha(criptografar("123456"), 10))
    response = client.put(
        "/recuperar-senha",
        json={
            "email": "ERRADO_email_9@teste.com",
            "token": "123456",
            "senhaNova": "senha_9",
        },
    )
    assert response.status_code == 400
    assert response.json == {"msg": "token ou email incorreto"}


def test_put_recuperar_senha_token_errado(client, database_session):
    response = client.put(
        "/recuperar-senha",
        json={
            "email": "email_9@teste.com",
            "token": "000000",
            "senhaNova": "senha_9",
        },
    )
    assert response.status_code == 400
    assert response.json == {"msg": "token ou email incorreto"}
