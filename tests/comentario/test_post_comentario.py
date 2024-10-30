from src.utils.jwt import gerar as gerar_token


def test_post_comentario(client, login):
    token = login("email_1@teste.com", "senha_1")
    response = client.post(
        "/comentario",
        json={
            "reclamacao": "1",
            "texto": "comentario teste",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert sorted(response.json.keys()) == [
        "criacao",
        "foto",
        "id_comenatario",
        "id_usuario",
        "nome",
        "texto",
    ]


def test_post_comentario_reclamacao_nao_encontrada(client, login):
    token = login("email_1@teste.com", "senha_1")
    response = client.post(
        "/comentario",
        json={
            "reclamacao": "999",
            "texto": "comentario teste",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert response.json == {"msg": "reclamacao nao encontrada"}


def test_post_comentario_usuario_nao_encontrada(client):
    token = gerar_token({"id": "9999"})
    response = client.post(
        "/comentario",
        json={
            "reclamacao": "1",
            "texto": "comentario teste",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert response.json == {"msg": "usuario nao encontrado"}
