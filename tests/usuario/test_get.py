from src.utils.jwt import gerar as gerar_token


def test_get(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.get("/usuario", headers={"Authorization": f"Bearer {token}"})
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


def test_get_nao_encontrado(client):
    token = gerar_token({"id": "9999"})
    response = client.get("/usuario", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json == {"msg": "usuario nao encontrado"}


def test_get_sem_token(client):
    response = client.get("/usuario")
    assert response.status_code == 401
    assert response.json == {"msg": "Está faltando o token"}


def test_get_token_invalido(client, token_falso):
    token = token_falso(0)
    response = client.get("/usuario", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json == {"msg": "Token inválido"}
