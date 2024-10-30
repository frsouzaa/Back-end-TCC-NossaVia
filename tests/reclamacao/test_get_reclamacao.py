def test_get_reclamacao_id(client):
    response = client.get("/reclamacao?id=2")
    assert response.status_code == 200
    assert sorted(response.json.keys()) == [
        "bairro",
        "categoria",
        "cep",
        "cidade",
        "criacao",
        "curtido",
        "data",
        "descricao",
        "endereco",
        "estado",
        "foto_usuario",
        "fotos",
        "id",
        "latitude",
        "longitude",
        "nome_usuario",
        "numero_endereco",
        "ponto_referencia",
        "qtd_curtidas",
        "status",
    ]


def test_get_reclamacao_id_usuario_logado(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.get(
        "/reclamacao?id=2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert sorted(response.json.keys()) == [
        "bairro",
        "categoria",
        "cep",
        "cidade",
        "criacao",
        "curtido",
        "data",
        "descricao",
        "endereco",
        "estado",
        "foto_usuario",
        "fotos",
        "id",
        "latitude",
        "longitude",
        "nome_usuario",
        "numero_endereco",
        "ponto_referencia",
        "qtd_curtidas",
        "status",
    ]


def test_get_reclamacao(client):
    response = client.get("/reclamacao?latitude=0&longitude=0&page=0&categoria=via")
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
            "qtd_curtidas",
            "status",
        ]


def test_get_reclamacao_sem_categoria(client):
    response = client.get("/reclamacao?latitude=0&longitude=0&page=0")
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
            "qtd_curtidas",
            "status",
        ]


def test_get_reclamacao_usuario_logado(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.get(
        "/reclamacao?latitude=0&longitude=0&page=0",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    for json in response.json:
        assert sorted(json.keys()) == [
            "categoria",
            "curtido",
            "descricao",
            "endereco",
            "foto_usuario",
            "fotos",
            "id",
            "nome_usuario",
            "numero_endereco",
            "page",
            "qtd_curtidas",
            "status",
        ]


def test_get_reclamacao_categoria_invalida(client):
    response = client.get("/reclamacao?latitude=0&longitude=0&page=0&categoria=teste")
    assert response.status_code == 409
    assert response.json == {"msg": "categoria invalida"}


def test_get_reclamacao_sem_parametros(client):
    response = client.get("/reclamacao")
    assert response.status_code == 409
    assert response.json == {"msg": "parametros invalidos"}


def test_get_reclamacao_usuario_inexistente(client):
    response = client.get("/reclamacao?id=9999")
    assert response.status_code == 404
    assert response.json == {"msg": "reclamacao nao encontrada"}
