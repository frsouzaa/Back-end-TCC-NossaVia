import base64
from src.utils.jwt import gerar as gerar_token
from azure.storage.blob import BlobClient


def test_post_denuncia(monkeypatch, client, login):
    def upload_blob_mock(self, image_data, blob_type):
        return None

    monkeypatch.setattr(BlobClient, "upload_blob", upload_blob_mock)

    image_path = "tests/assets/foto_usuario.png"
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    base64_encoded_data = base64.b64encode(image_data)
    base64_string = base64_encoded_data.decode("utf-8")

    token = login("email_10@teste.com", "senha_10")
    response = client.post(
        "/denuncia",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "descricao": "descricao teste",
            "categoria": "via",
            "data": "2024-09-25 23:13:00.000000",
            "endereco": "rua teste",
            "numero_endereco": "123",
            "ponto_referencia": "perto do teste",
            "cep": "12345-123",
            "latitude": "-1234567890",
            "longitude": "-1234567890",
            "fotos": [base64_string],
        },
    )
    assert response.status_code == 201
    assert response.json == {"msg": "criado"}


def test_post_denuncia_categoria_invalida(client, login):
    image_path = "tests/assets/foto_usuario.png"
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    base64_encoded_data = base64.b64encode(image_data)
    base64_string = base64_encoded_data.decode("utf-8")

    token = login("email_10@teste.com", "senha_10")
    response = client.post(
        "/denuncia",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "descricao": "descricao teste",
            "categoria": "nao_existe",
            "data": "2024-09-25 23:13:00.000000",
            "endereco": "rua teste",
            "numero_endereco": "123",
            "ponto_referencia": "perto do teste",
            "cep": "12345-123",
            "latitude": "-1234567890",
            "longitude": "-1234567890",
            "fotos": [base64_string],
        },
    )
    assert response.status_code == 409
    assert response.json == {"msg": "categoria invalida"}


def test_post_denuncia_data_invalida(client, login):
    image_path = "tests/assets/foto_usuario.png"
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    base64_encoded_data = base64.b64encode(image_data)
    base64_string = base64_encoded_data.decode("utf-8")

    token = login("email_10@teste.com", "senha_10")
    response = client.post(
        "/denuncia",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "descricao": "descricao teste",
            "categoria": "via",
            "data": "teste_data_invalida",
            "endereco": "rua teste",
            "numero_endereco": "123",
            "ponto_referencia": "perto do teste",
            "cep": "12345-123",
            "latitude": "-1234567890",
            "longitude": "-1234567890",
            "fotos": [base64_string],
        },
    )
    assert response.status_code == 409
    assert response.json == {"msg": "data invalida"}


def test_post_denuncia_usuario_inexistente(client, login):
    image_path = "tests/assets/foto_usuario.png"
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    base64_encoded_data = base64.b64encode(image_data)
    base64_string = base64_encoded_data.decode("utf-8")

    token = gerar_token({"id": "9999"})
    response = client.post(
        "/denuncia",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "descricao": "descricao teste",
            "categoria": "via",
            "data": "2024-09-25 23:13:00.000000",
            "endereco": "rua teste",
            "numero_endereco": "123",
            "ponto_referencia": "perto do teste",
            "cep": "12345-123",
            "latitude": "-1234567890",
            "longitude": "-1234567890",
            "fotos": [base64_string],
        },
    )
    assert response.status_code == 409
    assert response.json == {"msg": "usuario inexistente"}
