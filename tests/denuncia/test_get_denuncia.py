def test_get_denuncia_id(client):
    response = client.get("/denuncia?id=2")
    assert response.status_code == 200
    assert sorted(response.json.keys()) == [
        "categoria",
        "cep",
        "criacao",
        "data",
        "descricao",
        "endereco",
        "fotos",
        "id",
        "latitude",
        "longitude",
        "numero_endereco",
        "ponto_referencia",
        "qtd_curtidas",
        "status",
    ]


def test_get_denuncia(client):
    response = client.get("/denuncia?latitude=0&longitude=0&page=0&categoria=via")
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


def test_get_denuncia_sem_categoria(client):
    response = client.get("/denuncia?latitude=0&longitude=0&page=0")
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


def test_get_denuncia_categoria_invalida(client):
    response = client.get("/denuncia?latitude=0&longitude=0&page=0&categoria=teste")
    assert response.status_code == 409
    assert response.json == {"msg": "categoria invalida"}


def test_get_denuncia_sem_parametros(client):
    response = client.get("/denuncia")
    assert response.status_code == 409
    assert response.json == {"msg": "parametros invalidos"}


def test_get_denuncia_usuario_inexistente(client):
    response = client.get("/denuncia?id=9999")
    assert response.status_code == 404
    assert response.json == {"msg": "denuncia nao encontrada"}
