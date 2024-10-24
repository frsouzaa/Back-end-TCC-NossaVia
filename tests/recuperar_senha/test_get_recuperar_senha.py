from src.db.database import RecuperarSenha
from src.utils.senha import criptografar


def test_get_recuperar_senha(client, database_session):
    database_session.add(RecuperarSenha(criptografar("123456"), 9))
    response = client.get(
        "/recuperar-senha?email=email_8@teste.com&token=123456",
    )
    assert response.status_code == 200
    assert response.json == {"msg": "token valido"}


def teste_get_recuperar_senha_email_invalido(client):
    response = client.get(
        "/recuperar-senha?email=email_8888@teste.com&token=123456",
    )
    assert response.status_code == 409
    assert response.json == {"msg": "token ou email incorreto"}


def teste_get_recuperar_senha_token_invalido(client):
    response = client.get(
        "/recuperar-senha?email=email_8@teste.com&token=000000",
    )
    assert response.status_code == 409
    assert response.json == {"msg": "token ou email incorreto"}
