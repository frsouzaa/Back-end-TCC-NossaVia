from src.utils.jwt import gerar as gerar_token
import base64
from azure.storage.blob import BlobClient


def test_put_usuario(monkeypatch, client, login):
    def upload_blob_mock(self, image_data, blob_type):
        return None

    monkeypatch.setattr(BlobClient, "upload_blob", upload_blob_mock)

    image_path = "tests/assets/foto_usuario.png"
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    base64_encoded_data = base64.b64encode(image_data)
    base64_string = base64_encoded_data.decode("utf-8")

    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/usuario",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "usuario",
            "endereco": "rua",
            "cep": "00000-000",
            "numero_endereco": "0",
            "complemento_endereco": "",
            "data_nascimento": "2004-06-15 00:00:00.000000",
            "sexo": "m",
            "telefone": "11 11111-1111",
            "foto": base64_string,
        },
    )
    assert response.status_code == 200
    assert sorted(response.json.keys()) == [
        "cep",
        "complemento_endereco",
        "data_nascimento",
        "email",
        "endereco",
        "foto",
        "nome",
        "numero_endereco",
        "pontucao",
        "sexo",
        "telefone",
    ]


def test_put_usuario_sem_foto(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/usuario",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "usuario",
            "endereco": "rua",
            "cep": "00000-000",
            "numero_endereco": "0",
            "complemento_endereco": "",
            "data_nascimento": "2004-06-15 00:00:00.000000",
            "sexo": "m",
            "telefone": "11 11111-1111",
            "foto": None,
        },
    )
    assert response.status_code == 200
    assert sorted(response.json.keys()) == [
        "cep",
        "complemento_endereco",
        "data_nascimento",
        "email",
        "endereco",
        "foto",
        "nome",
        "numero_endereco",
        "pontucao",
        "sexo",
        "telefone",
    ]


def test_put_usuario_sem_body(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/usuario",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )
    assert response.status_code == 200
    assert response.json == {"msg": "nada foi alterado"}


def test_put_usuario_nao_encontrado(client):
    token = gerar_token({"id": "9999"})
    response = client.put(
        "/usuario",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )
    assert response.status_code == 404
    assert response.json == {"msg": "usuario nao encontrado"}
