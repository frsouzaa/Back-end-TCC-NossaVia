def test_delete_comentario(client, login):
    token = login("email_1@teste.com", "senha_1")
    response = client.delete(
        "/comentario?id=2", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json == {"msg": "comentario deletado com sucesso"}


def test_delete_comentario_com_id_invalido(client, login):
    token = login("email_1@teste.com", "senha_1")
    response = client.delete(
        "/comentario?id=999", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json == {"msg": "comentario nao encontrado"}
