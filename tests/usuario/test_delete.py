from src.utils.jwt import gerar as gerar_token


def test_delete_usuario(client, login):
    token = login("email_0@teste.com", "senha_0")
    response = client.delete("/usuario", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json == {"msg": "deletado"}


def test_delete_usuario_nao_encontrado(client):
    token = gerar_token({"id": "9999"})
    response = client.delete("/usuario", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json == {"msg": "usuario nao encontrado"}
