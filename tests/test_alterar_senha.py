def test_alterar_senha(client, login):
    token = login("email_9@teste.com", "senha_9")
    response = client.post(
        "/alterar-senha",
        headers={"Authorization": f"Bearer {token}"},
        json={"senhaAtual": "senha_9", "senhaNova": "senha_99"},
    )
    assert response.status_code == 200
    assert response.json == {"msg": "senha alterada"}


def test_alterar_senha_senha_atual_incorreta(client, login):
    token = login("email_9@teste.com", "senha_99")
    response = client.post(
        "/alterar-senha",
        headers={"Authorization": f"Bearer {token}"},
        json={"senhaAtual": "senha_9", "senhaNova": "senha_99"},
    )
    assert response.status_code == 400
    assert response.json == {"msg": "senha atual incorreta"}