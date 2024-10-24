from smtplib import SMTP_SSL
from unittest import mock
import os


def test_post_recuperar_senha(monkeypatch, client):
    def enter_mock(self):
        return SMTP_SSL()

    def login_mock(self, email, senha):
        pass

    def send_message_mock(self, msg):
        pass

    monkeypatch.setattr(SMTP_SSL, "__enter__", enter_mock)
    monkeypatch.setattr(SMTP_SSL, "login", login_mock)
    monkeypatch.setattr(SMTP_SSL, "send_message", send_message_mock)

    response = client.post("/recuperar-senha", json={"email": "email_7@teste.com"})
    assert response.status_code == 200
    assert response.json == {"msg": "token gerado"}


def test_post_recuperar_senha_erro_email_nao_encontrado(client):
    response = client.post(
        "/recuperar-senha", json={"email": "NAO_ENCONTRADO_email_7@teste.com"}
    )
    assert response.status_code == 409
    assert response.json == {"msg": "email nao encontrado"}


def test_post_recuperar_senha_erro_ao_enviar_email(client):
    with mock.patch.dict(os.environ, {"EMAIL": "", "SENHA": ""}):
        response = client.post("/recuperar-senha", json={"email": "email_7@teste.com"})
        assert response.status_code == 520
        assert response.json == {"msg": "nao foi possivel enviar o email nesse momento"}
