def test_post_curtida_nova(client, login):
    token = login("email_1@teste.com", "senha_1")
    response = client.post(
        "/curtida",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "reclamacao": "1",
        },
    )
    assert response.status_code == 201
    assert response.json == {"mensagem": "curtida realizada com sucesso"}


def test_post_curtida_existente(client, login):
    token = login("email_1@teste.com", "senha_1")
    response = client.post(
        "/curtida",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "reclamacao": "1",
        },
    )
    assert response.status_code == 409
    assert response.json == {"mensagem": "reclamacao ja curtida pelo usuario"}


def test_post_curtida_reclamacao_nao_encontrada(client, login):
    token = login("email_1@teste.com", "senha_1")
    response = client.post(
        "/curtida",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "reclamacao": "999",
        },
    )
    assert response.status_code == 404
    assert response.json == {"mensagem": "reclamacao nao encontrada"}


def test_delete_curtida(client, login):
    token = login("email_1@teste.com", "senha_1")
    response = client.delete(
        "/curtida?reclamacao=1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json == {"mensagem": "curtida removida com sucesso"}


def test_delete_curtida_nao_existente(client, login):
    token = login("email_1@teste.com", "senha_1")
    response = client.delete(
        "/curtida?reclamacao=1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 409
    assert response.json == {"mensagem": "reclamacao nao estava curtida pelo usuario"}


def teste_post_curtida_deletada(client, login):
    token = login("email_1@teste.com", "senha_1")
    response = client.post(
        "/curtida",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "reclamacao": "1",
        },
    )
    assert response.status_code == 200
    assert response.json == {"mensagem": "curtida realizada com sucesso"}
