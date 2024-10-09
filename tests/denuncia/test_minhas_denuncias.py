def test_get_minhas_denuncias(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.get(
        "/minhas-denuncias?page=0",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    for json in response.json:
        assert sorted(json.keys()) == [
            "categoria",
            "descricao",
            "endereco",
            "foto_usuario",
            "fotos",
            "id",
            "nome_usuario",
            "numero_endereco",
            "page",
            "status",
        ]

def test_get_minhas_denuncias_com_categoria(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.get(
        "/minhas-denuncias?page=0&categoria=via",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    for json in response.json:
        assert sorted(json.keys()) == [
            "categoria",
            "descricao",
            "endereco",
            "foto_usuario",
            "fotos",
            "id",
            "nome_usuario",
            "numero_endereco",
            "page",
            "status",
        ]

def test_get_minhas_denuncias_com_categoria_invalida(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.get(
        "/minhas-denuncias?page=0&categoria=teste",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409
    assert response.json == {"msg": "categoria invalida"}
