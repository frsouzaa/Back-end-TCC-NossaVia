def test_delete_reclamacao(client, login):
    token = login("email_0@teste.com", "senha_0")
    response = client.delete(
        "/reclamacao?id=1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json == {"msg": "deletado"}


def test_delete_reclamacao_nao_encontrada(client, login):
    token = login("email_0@teste.com", "senha_0")
    response = client.delete(
        "/reclamacao?id=999", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json == {"msg": "reclamacao nao encontrada"}
